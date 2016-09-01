#!/bin/bash
###########################################################################
#    > File Name: run.sh
#    > Author: zhangminghua
#    > Mail: zhangmh1993@163.com
#    > Created Time: 2016.8.30 10:21:06
###########################################################################

set -x
set -u

source run.conf
date +'%Y.%m.%d %H:%M:%S'


############################ 第一阶段 : 预料去重
if [ $run_uniq -eq 1 ]; then
    cat ${input_0} | awk -F '\t' '{print $2}' > temp
    sort temp > ${output_sort}
    uniq ${output_sort} > ${output_0}
    rm ${output_sort} temp
fi


############################ 第一阶段 : 预料预处理
if [ $run_preprocess -eq 1 ]; then
    ${python} ./script/preprocess_corpus_1.py ${input_1} ${output_1} 2>&1 > ${log}/log.1
    if [ $? -ne 0 ]; then
        echo "preprocess error"
        exit 1
    else
        echo "preprocess complete"
    fi
fi


############################ 第一阶段 : ansj分词
if [ $run_seg -eq 1 ]; then
    cd ${path}/ansj
    ./user_dic_2_0.sh ${input_2} ${python} 2>&1 > ${log}/log.2
    if [ $? -ne 0 ]; then
        echo "user_dic error"
        exit 1
    else
        echo "user_dic complete"
    fi    
    ./ansj_seg_2.sh ${input_2} ${output_2} ${config} 2>&1 >> ${log}/log.2
    if [ $? -ne 0 ]; then
        echo "ansj error"
        exit 1
    else
        echo "ansj complete"
    fi
    cd ${path}
fi


############################ 第一阶段 : 计算关键词
if [ $run_key_word -eq 1 ]; then
    ${python} ./script/key_word_3.py ${input_3} ${output_3} ${stopword} ${config} 2>&1 > ${log}/log.3
    if [ $? -ne 0 ]; then
        echo "key_word error"
        exit 1
    else
        echo "key_word complete"
    fi
fi


############################ 第一阶段 : 分桶,计算句对相似性
if [ $run_pair_sim -eq 1 ]; then
    ${python} ./script/ne_bucket_4_0.py ${input_4} ${ltp_model} ${config} 2>&1 > ${log}/log.4
    if [ $? -ne 0 ]; then
        echo "ne_bucket error"
        exit 1
    else
        echo "ne_bucket complete"
    fi
    ${python} ./script/pair_sim_4.py ${input_4} ${log} ${config} 2>&1 >> ${log}/log.4
    if [ $? -ne 0 ]; then
        echo "pair_sim error"
        exit 1
    else
        echo "pair_sim complete"
    fi
    cat ${input_4}.*.sim > ${output_4}
    rm ${input_4}.*.sim
fi


############################ 第一阶段 : 平行句对筛选与分离
if [ $run_split_para -eq 1 ]; then
    ${python} ./script/split_para_5.py ${input_5} ${output_source_5} ${output_target_5} ${config} 2>&1 > ${log}/log.5
    if [ $? -ne 0 ]; then
        echo "split_para error"
        exit 1
    else
        echo "split_para complete"
    fi
    ${python} ./script/pair_merge_5_1.py ${output_source_5} ${output_target_5} ${source_lib} ${target_lib} ${config} 2>&1 > ${log}/log.5.1
    if [ $? -ne 0 ]; then
        echo "pair_merge error"
        exit 1
    else
        echo "pair_merge complete"
    fi
fi


############################ 第二阶段 : StanfordParser抽取短语对
if [ $run_parser -eq 1 ]; then
    cd ${path}/StanfordParser
    if [ ${is_full_parser} -eq 1 ]; then
        input_source_6=${source_lib}
        input_target_6=${target_lib}
    fi
    
    ./stanford_parser_6.sh ${input_source_6} ${input_target_6} ${output_6} ${config} 2>&1 > ${log}/log.6
    if [ $? -ne 0 ]; then
        echo "parser error"
        exit 1
    else
        echo "parser complete"
    fi
    cd ${path}
fi


############################ 第二阶段 : 简单规则过滤
if [ $run_simple_filter -eq 1 ]; then
    ${python} ./script/phrase_pivot_7_0.py ${input_7} ${output_pivot} ${is_phrase_pivot} ${config} 2>&1 > ${log}/log.7
    if [ $? -ne 0 ]; then
        echo "phrase_pivot error"
        exit 1
    else
        echo "phrase_pivot complete"
    fi
    ${python} ./script/filter_phrase_7.py ${output_pivot} ${output_7} ${lm_model} ${wordnet} ${config} 2>&1 >> ${log}/log.7
    if [ $? -ne 0 ]; then
        echo "filter_phrase error"
        exit 1
    else
        echo "filter_phrase complete"
    fi
fi


############################ 第三阶段 : 分布相似度过滤
if [ $run_context_extract -eq 1 ]; then
    cat ${input_source_6} ${input_target_6} ${context} > temp
    sort temp > ${context}
    uniq ${context} > temp
    ./script/shuffle.sh temp > ${context}
    rm temp

    ${python} ./script/context_extract_8.py ${input_8} ${output_8} ${context} ${config} 2>&1 > ${log}/log.8
    if [ $? -ne 0 ]; then
        echo "context_extract error"
        exit 1
    else
        echo "context_extract complete"
    fi

    ${python} ./script/para_merge_8_1.py ${output_8} ${para_lib} ${config} 2>&1 > ${log}/log.8.1
    if [ $? -ne 0 ]; then
        echo "para_merge error"
        exit 1
    else
        echo "para_merge complete"
    fi
fi


date +'%Y.%m.%d %H:%M:%S'

