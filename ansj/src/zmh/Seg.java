package zmh;

import org.ho.yaml.Yaml;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.DicAnalysis;
import org.ansj.splitWord.analysis.ToAnalysis;

public class Seg {

    HashMap config;
    Seg(String fyaml){
        try {
            config = Yaml.loadType(new File(fyaml), HashMap.class);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

	// 携程语料相关问题对
	void readRelevance(String relfile) {
		try {
			FileReader reader = new FileReader(relfile);
			BufferedReader br = new BufferedReader(reader);
			FileWriter writer = new FileWriter(relfile + "_seg");
			BufferedWriter bw = new BufferedWriter(writer);

			String line;
			while (true) {
				line = br.readLine();
				if (line == null)
					break;
				String[] org = line.trim().split("\t");
				Result oterm = ToAnalysis.parse(org[1]);
				bw.write(org[0] + "\t");
				for (Term term : oterm) {
					bw.write(term.getName().trim() + ",");
				}
				bw.write("\n*********************************\n");
				br.readLine();
				while (true) {
					line = br.readLine();
					// System.out.println(line);
					if (line.indexOf("%%") != 0)
						break;
					String[] rel = line.substring(2).trim().split("\t");
					Result rterm = ToAnalysis.parse(rel[1]);
					bw.write("%%" + rel[0] + "\t");
					for (Term term : rterm) {
						bw.write(term.getName().trim() + ",");
					}
					bw.write("\n");
				}
				bw.write("\n");
			}
			br.close();
			reader.close();
			bw.close();
			writer.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	// 携程语料候选问题对
	void readCandidate(String canfile) {
		try {
			FileReader reader = new FileReader(canfile);
			BufferedReader br = new BufferedReader(reader);
			FileWriter writer = new FileWriter(canfile + "_seg");
			BufferedWriter bw = new BufferedWriter(writer);
			FileWriter iwriter = new FileWriter("index.txt");
			BufferedWriter ibw = new BufferedWriter(iwriter);

			String line;
			int i = 0;
			int[] index = new int[39930];
			while (true) {
				line = br.readLine();
				if (line == null)
					break;
				String[] org = line.trim().split("\t");
				index[i++] = Integer.parseInt(org[0]);

				Result oterm = ToAnalysis.parse(org[1]);
				bw.write(org[0] + "\t");
				for (Term term : oterm) {
					bw.write(term.getName().trim() + ",");
				}
				bw.write("\n*********************************\n");
				br.readLine();
				while (true) {
					line = br.readLine();
					if (line.indexOf("\t") < 0)
						break;
					String[] rel = line.trim().split("\t");
					index[i++] = Integer.parseInt(rel[0]);

					Result rterm = ToAnalysis.parse(rel[1]);
					bw.write(rel[0] + "\t");
					for (Term term : rterm) {
						bw.write(term.getName().trim() + ",");
					}
					bw.write("\n");
				}
				bw.write("\n");
			}

			Arrays.sort(index);
			ibw.write(Integer.toString(i) + "\n");
			for (int x : index) {
				ibw.write(Integer.toString(x) + "\n");
			}

			br.close();
			reader.close();
			bw.close();
			writer.close();
			ibw.close();
			iwriter.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	// 问答对语料
	void readCorpus(String infile, String outfile,int num) {
		try {
			FileReader reader = new FileReader(infile);
			BufferedReader br = new BufferedReader(reader);
			FileWriter writer = new FileWriter(outfile);
			BufferedWriter bw = new BufferedWriter(writer);
			FileWriter lwriter = new FileWriter(infile + ".len");
			BufferedWriter lbw = new BufferedWriter(lwriter);
			
			String line;
			int len;
			while (true) {
				line = br.readLine();
				if (line == null)
					break;
				String[] qa = line.trim().split("\t");
				
				for(int i=0;i<num;i++){
                    //System.out.println(qa[i]);
					Result terms = DicAnalysis.parse(qa[i]);
					len = 0;
					for (Term term : terms) {
						if(term.getNatureStr() != "null"){
							len += 1;
							bw.write(term.getName().trim()+(char)((int)config.get("sep_1"))+term.getNatureStr()+(String)config.get("sep_w"));
						}
					}
					lbw.write(Integer.toString(len));
					if(i != num-1){
						bw.write("\t");
						lbw.write("\t");
					}
				}
				lbw.write("\n");
				bw.write("\n");
			}
			br.close();
			reader.close();
			bw.close();
			writer.close();
			lbw.close();
			lwriter.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		long begin = System.currentTimeMillis();
		Seg seg=new Seg(args[2]); 
	    seg.readCorpus(args[0], args[1], 1);
		long end = System.currentTimeMillis();
		System.out.println("Complete! Cost：" + (end-begin) + "ms");
	}
}
