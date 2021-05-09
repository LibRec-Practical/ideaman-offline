import numpy as np
import tensorflow as tf
from keras import initializers
from keras.models import Model
from keras.layers import Embedding, Input, Dense, Flatten, concatenate, Dot, Lambda, multiply, Reshape, multiply
from keras.optimizers import Adagrad, Adam, SGD, RMSprop
from keras import backend as K
from DeepCF.evaluate import evaluate_model
from DeepCF.Dataset import Dataset
from time import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Run DeepF.")
    parser.add_argument('--path', nargs='?', default='Data/',
                        help='Input data path.')
    parser.add_argument('--dataset', nargs='?', default='ml-1m',
                        help='Choose a dataset.')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Number of epochs.')
    parser.add_argument('--batch_size', type=int, default=256,
                        help='Batch size.')
    parser.add_argument('--layers', nargs='?', default='[512,256,128,64]',
                        help="MLP layers. Note that the first layer is the concatenation "
                             "of user and item embeddings. So layers[0]/2 is the embedding size.")
    parser.add_argument('--userlayers', nargs='?', default='[512, 64]',
                        help="Size of each user layer")
    parser.add_argument('--itemlayers', nargs='?', default='[1024, 64]',
                        help="Size of each item layer")
    parser.add_argument('--num_neg', type=int, default=4,
                        help='Number of negative instances to pair with a positive instance.')
    parser.add_argument('--lr', type=float, default=0.0001,
                        help='Learning rate.')
    parser.add_argument('--learner', nargs='?', default='sgd',
                        help='Specify an optimizer: adagrad, adam, rmsprop, sgd')
    parser.add_argument('--verbose', type=int, default=1,
                        help='Show performance per X iterations')
    parser.add_argument('--out', type=int, default=1,
                        help='Whether to save the trained model.')
    parser.add_argument('--dmf_pretrain', nargs='?', default='',
                        help='Specify the pretrain model file for DMF part. If empty, no pretrain will be used')
    parser.add_argument('--mlp_pretrain', nargs='?', default='',
                        help='Specify the pretrain model file for MLP part. If empty, no pretrain will be used')
    return parser.parse_args()


def get_model(train, num_users, num_items, userlayers, itemlayers, layers):
    dmf_num_layer = len(userlayers) #Number of layers in the DMF
    mlp_num_layer = len(layers) #Number of layers in the MLP
    user_matrix = K.constant(getTrainMatrix(train))
    item_matrix = K.constant(getTrainMatrix(train).T)
    # Input variables
    user_input = Input(shape=(1,), dtype='int32', name='user_input')
    item_input = Input(shape=(1,), dtype='int32', name='item_input')
    
    # Embedding layer
    user_rating= Lambda(lambda x: tf.gather(user_matrix, tf.compat.v1.to_int32(x)))(user_input)
    item_rating = Lambda(lambda x: tf.gather(item_matrix, tf.compat.v1.to_int32(x)))(item_input)
    user_rating = Reshape((num_items, ))(user_rating)
    item_rating = Reshape((num_users, ))(item_rating)

    # DMF part
    userlayer = Dense(userlayers[0],  activation="linear" , name='user_layer0')
    itemlayer = Dense(itemlayers[0], activation="linear" , name='item_layer0')
    dmf_user_latent = userlayer(user_rating)
    dmf_item_latent = itemlayer(item_rating)
    for idx in range(1, dmf_num_layer):
        userlayer = Dense(userlayers[idx],  activation='relu', name='user_layer%d' % idx)
        itemlayer = Dense(itemlayers[idx],  activation='relu', name='item_layer%d' % idx)
        dmf_user_latent = userlayer(dmf_user_latent)
        dmf_item_latent = itemlayer(dmf_item_latent)
    dmf_vector = multiply([dmf_user_latent, dmf_item_latent])

    # MLP part 
    MLP_Embedding_User = Dense(layers[0]//2, activation="linear" , name='user_embedding')
    MLP_Embedding_Item  = Dense(layers[0]//2, activation="linear" , name='item_embedding')
    mlp_user_latent = MLP_Embedding_User(user_rating)
    mlp_item_latent = MLP_Embedding_Item(item_rating)
    mlp_vector = concatenate([mlp_user_latent, mlp_item_latent])
    for idx in range(1, mlp_num_layer):
        layer = Dense(layers[idx], activation='relu', name="layer%d" % idx)
        mlp_vector = layer(mlp_vector)

    # Concatenate DMF and MLP parts
    predict_vector = concatenate([dmf_vector, mlp_vector])
    
    # Final prediction layer
    prediction = Dense(1, activation='sigmoid', kernel_initializer=initializers.lecun_normal(),
                       name="prediction")(predict_vector)
    
    model_ = Model(inputs=[user_input, item_input],
                   outputs=prediction)
    
    return model_

def getTrainMatrix(train):
    num_users, num_items = train.shape
    train_matrix = np.zeros([num_users, num_items], dtype=np.int32)
    for (u, i) in train.keys():
        train_matrix[u][i] = 1
    return train_matrix




def get_train_instances(train):
    user_input, item_input, labels = [], [], []
    num_users = train.shape[0]
    for (u, i) in train.keys():
        # positive instance
        user_input.append(u)
        item_input.append(i)
        labels.append(1)
       
    return user_input, item_input, labels


def main():
    args = parse_args()
    userlayers = eval(args.userlayers)
    itemlayers = eval(args.itemlayers)
    layers = eval(args.layers)
    learner = args.learner
    learning_rate = args.lr
    batch_size = args.batch_size
    num_epochs = args.epochs
    verbose = args.verbose
    dmf_pretrain = args.dmf_pretrain
    mlp_pretrain = args.mlp_pretrain
            
    dataset = "ml-1m"
    epochs=100
    lr=0.01

    topK = 10 #取前十个
    evaluation_threads = 1  # mp.cpu_count()
    model_out_file = 'Pretrain/%s_CFNet_%d.h5' %(args.dataset, time())

    # 加载数据
    t1 = time()
    dataset = Dataset()
    train, testRatings,testNegatives = dataset.trainMatrix, dataset.testRatings ,dataset.testNegatives
    num_users, num_items = train.shape
    print("Load data done [%.1f s]. #user=%d, #item=%d, #train=%d, #test=%d" 
          %(time()-t1, num_users, num_items, train.nnz, len(testRatings)))
    
    # Build model
    model = get_model(train, num_users, num_items, userlayers, itemlayers, layers)
    if learner.lower() == "adagrad": 
        model.compile(optimizer=Adagrad(lr=learning_rate), loss='binary_crossentropy')
    elif learner.lower() == "rmsprop":
        model.compile(optimizer=RMSprop(lr=learning_rate), loss='binary_crossentropy')
    elif learner.lower() == "adam":
        model.compile(optimizer=Adam(lr=learning_rate), loss='binary_crossentropy')
    else:
        model.compile(optimizer=SGD(lr=learning_rate), loss='binary_crossentropy')

    # Training model
    for epoch in range(num_epochs):
        t1 = time()
        # Generate training instances
        user_input, item_input, labels = get_train_instances(train)
        
        # Training
        hist = model.fit([np.array(user_input), np.array(item_input)],  # input
                         np.array(labels),  # labels
                         batch_size=batch_size, epochs=1, verbose=0, shuffle=True)
        
    evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)

if __name__ == '__main__':
    main()