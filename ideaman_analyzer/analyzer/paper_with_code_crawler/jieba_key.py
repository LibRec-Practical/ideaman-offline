import RAKE as rake
import stop_words

stop_words = stop_words.safe_get_stop_words('en')

if __name__ == '__main__':
    rake_obj = rake.Rake(stop_words)
    sample_file = open("./QA_papers.txt", 'r')
    text = sample_file.read()
    keywords = rake_obj.run(text, 5, 3, 20)

    # 3. print results
    for i in keywords:
        print(i)
