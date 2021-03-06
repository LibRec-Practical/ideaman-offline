package Sort;

import net.librec.common.LibrecException;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Map;

public interface Sort{
    public void train();
    public Map<String,Double> predict(String paper_id);
    public void run() throws IOException, LibrecException;
}
