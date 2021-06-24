package Recall;

import net.librec.common.LibrecException;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Map;

interface Recall{
    public void train();
    public Map<String,Double> predict(String paper_id);
    public void run() throws LibrecException, IOException, SQLException;
}