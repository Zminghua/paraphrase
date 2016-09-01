
import org.ho.yaml.Yaml;
import java.util.ArrayList;
import java.util.Arrays;
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
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

class Parser {
	
	//NP		VP		LCP			PP	
	//名词短语	动词短语	方位词短语	介词短语
	//CP							DNP
	//由‘的’构成的表示修饰性关系的短语	由‘的’构成的表示所属关系的短语,
	//ADVP		ADJP		DP			QP
	//副词短语	形容词短语	限定词短语	量词短语
	
	HashSet<String> PT;
	HashMap<String,HashSet<String>> lineP;
    HashMap config;

	Parser(String fyaml){
		PT = new HashSet<String>(Arrays.asList("NN","NR","VV","NP", "VP","ADJP"));
		lineP = new HashMap<String,HashSet<String>>();
        try {
            config = Yaml.loadType(new File(fyaml), HashMap.class);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
	
	void ParserIO(String enfile, String frfile, String outfile){
		String parserModel = "edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz";
        String[] options = {"-MAX_ITEMS","2000000"};
		LexicalizedParser lp = LexicalizedParser.loadModel(parserModel,options);
		try {
			FileReader enReader = new FileReader(enfile);
			BufferedReader en = new BufferedReader(enReader);
			FileReader frReader = new FileReader(frfile);
			BufferedReader fr = new BufferedReader(frReader);
			FileWriter writer = new FileWriter(outfile);
			BufferedWriter bw = new BufferedWriter(writer);

			String enline,frline;
			while (true) {
				enline = en.readLine();
				frline = fr.readLine();
				if (enline == null && frline == null)
					break;
                HashSet<String> enSet = parse(enline.trim(), lp);
                HashSet<String> frSet = parse(frline.trim(), lp);
                if(enSet.size() > 0 && frSet.size() > 0){
                    Iterator<String> enit=enSet.iterator();
                    while(enit.hasNext()){
                        String enphrase = enit.next().toString();
                        Iterator<String> frit=frSet.iterator();
                        while(frit.hasNext()){
                            String frphrase = frit.next().toString();
                            bw.write(enphrase+(String)(config.get("sep_p"))+frphrase+"\n");
                        }
                    }
                }
			}
			en.close();
			enReader.close();
			fr.close();
			frReader.close();
			bw.close();
			writer.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	HashSet<String> parse(String line, LexicalizedParser lp){
		if(lineP.get(line) == null){
			String[] sent = line.trim().split((String)config.get("sep_w"));
			List<CoreLabel> rawWords = Sentence.toCoreLabelList(sent);
			Tree syntax = lp.apply(rawWords);
			//syntax.pennPrint();
			HashSet<String> PhraseSet=new HashSet<String>();
			for(Tree subtree : syntax){
				if(PT.contains(subtree.label().toString())){
					String phrase = "";
                    int plen = 0;
					for(Tree leaf : subtree.getLeaves()){
                        String word = leaf.label().toString();
						phrase += word + (String)config.get("sep_w");
                        //plen += word.length();
                        plen += 1;
					}
                    if( plen <= (int)config.get("max_phrase_len") ){
					    PhraseSet.add(phrase.trim());
				    }
                }
			}
            lineP.put(line, PhraseSet);
		}
		return lineP.get(line);
	}
	
	/**
	 * Usage: {@code java ParserDemo [[model] textFile]}
	 * e.g.: java ParserDemo edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz data/chinese-onesent-utf8.txt
	 **/
	public static void main(String[] args) {
		long begin = System.currentTimeMillis();
		Parser parser = new Parser(args[3]);
		parser.ParserIO(args[0],args[1],args[2]);
		long end = System.currentTimeMillis();
		System.out.println("Complete! Cost：" + (end-begin)/1000.0 + "s");
	}
}
