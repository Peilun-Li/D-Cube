import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from DCube_params import *
from DCube_sql import *

import sys, os

DEBUG = 1
db_conn = None

def D_Cube_evaluation():

    k = 20
    # datasets = ['darpa']
    # density_measures = ['ari', 'geo', 'sus']
    # select_methods = ['card', 'dense']
    # datasets = ['darpa']
    datasets = ['airforce']
    density_measures = ['ari']
    select_methods = ['dense']

    # pos_total = int(get_first_res(db_conn, "select count(*) from darpa_sample where label !='-'"))
    # neg_total = int(get_first_res(db_conn, "select count(*) from darpa_sample where label ='-'"))
    pos_total = int(get_first_res(db_conn, "select count(*) from airforce_sample where label !='normal.'"))
    neg_total = int(get_first_res(db_conn, "select count(*) from airforce_sample where label ='normal.'"))
    
    if DEBUG:
        print 'pos_total=%s' % pos_total
        print 'neg_total=%s' % neg_total

    for ds in datasets:
        for dm in density_measures:
            for sm in select_methods:
                try:
                    
                    true_pos_kgroup, false_pos_kgroup, pos_dup_factor, neg_dup_factor, relation_results = get_results(ds, dm, sm, k)
                    if DEBUG:
                        print 'true_pos_kgroup=%s' % true_pos_kgroup
                        print 'false_pos_kgroup=%s' % false_pos_kgroup
                        print 'pos_dup_factor', pos_dup_factor
                        print 'neg_dup_factor', neg_dup_factor
                        pass
                    plot_ROC_curve(true_pos_kgroup, false_pos_kgroup, pos_total, neg_total, pos_dup_factor, neg_dup_factor, relation_results, k)
                    print 'Evaluation on %s_%s_%s Succeeded :) !' % (ds, dm, sm)
                    # exit(0)
                except: 
                    print 'Evaluation on %s_%s_%s failed !' % (ds, dm, sm)
                    print "Unexpected error:", sys.exc_info()



def get_results(dataset_name, density_measure, select_method, k):

    relation_paras = dataset_name + '_parameters_' + density_measure + '_' + select_method 
    relation_results = dataset_name + '_results_' + density_measure + '_' + select_method

    # Part 1
    true_pos_kgroup = {}
    false_pos_kgroup = {}



    try:
        cur = db_conn.cursor()
        # cur.execute("select block_idx, count(*) from %s where label !='-' group by block_idx ;" % relation_results)
        cur.execute("select block_idx, count(*) from %s where label !='normal.' group by block_idx ;" % relation_results)
        for record in cur:
            idx = int(record[0])
            count = int(record[1])
            true_pos_kgroup[idx] = count

        cur_false = db_conn.cursor()
        # cur_false.execute("select block_idx, count(*) from %s where label ='-' group by block_idx ;" % relation_results)
        cur_false.execute("select block_idx, count(*) from %s where label ='normal.' group by block_idx ;" % relation_results)
        for record in cur_false:
            idx = int(record[0])
            count = int(record[1])
            false_pos_kgroup[idx] = count
    except:
        print 'Access to results table %s failed !' % relation_results
        print "Unexpected error:", sys.exc_info()
        raise

    if 1 not in true_pos_kgroup:
        true_pos_kgroup[1] = 0;
    if 1 not in false_pos_kgroup:
        false_pos_kgroup[1] = 0;



    for i in range(2, k+1, 1):
        if i not in true_pos_kgroup:
            true_pos_kgroup[i] = true_pos_kgroup[i-1]
        else:
            true_pos_kgroup[i] = true_pos_kgroup[i-1] + true_pos_kgroup[i]
        if i not in false_pos_kgroup:
            false_pos_kgroup[i] = false_pos_kgroup[i-1]
        else:
            false_pos_kgroup[i] = false_pos_kgroup[i-1] + false_pos_kgroup[i]


    # Calculate duplicate factor 


    # try:
    #     pos_distinct_num = int(get_first_res(db_conn, "select count(*) from (select distinct source, destination, timestamp from %s where label !='-') as dis" % relation_results))
    #     pos_total_num = int(get_first_res(db_conn, "select count(*) from %s where label !='-'" % relation_results))
    #     pos_dup_factor  = float(pos_total_num) / pos_distinct_num
        
    #     neg_distinct_num = int(get_first_res(db_conn, "select count(*) from (select distinct source, destination, timestamp from %s where label ='-') as dis" % relation_results))
    #     neg_total_num = int(get_first_res(db_conn, "select count(*) from %s where label ='-'" % relation_results))
    #     neg_dup_factor = float(neg_total_num) / neg_distinct_num
    # except:
    #     print 'Access to calculate duplicate factor on results table %s failed !' % relation_results
    #     print "Unexpected error:", sys.exc_info()
    
    pos_dup_factor = 1.0
    neg_dup_factor = 1.0

    return true_pos_kgroup, false_pos_kgroup, pos_dup_factor, neg_dup_factor, relation_results


# def plot_ROC_curve(k, k_flags, k_values, pos_total, neg_total):
def plot_ROC_curve(true_pos_kgroup, false_pos_kgroup, pos_total, neg_total, pos_dup_factor, neg_dup_factor, relation_results, k):
    
    x = [false_pos_kgroup[i] / float(neg_total) for i in range(1, k+1)]
    y = [true_pos_kgroup[i] / float(pos_total) for i in range(1, k+1)]
    # x = [false_pos_kgroup[i] / float(neg_total * neg_dup_factor) for i in range(1, k+1)]
    # y = [true_pos_kgroup[i] / float(pos_total * pos_dup_factor) for i in range(1, k+1)]
    x = [i if i <= 1.0 else 1.0 for i in x]
    y = [i if i <= 1.0 else 1.0 for i in y]

    if DEBUG:
        print 'X=', x
        print 'Y=', y
    x.append(1.0)
    y.append(1.0)
    x.insert(0, 0.0)
    y.insert(0, 0.0)

    roc_auc = auc(x, y)
    
    lw = 2    
    plt.figure()
    plt.plot(x, y, color='darkorange', lw=lw, label='D-Cube')
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--', label='Random Guess')
    # plt.plot([],[],alpha=0.7, color='white', label='AUC = %0.3f' % roc_auc)
    plt.text(0.15, 0.9, 'AUC = %0.3f' % roc_auc, fontsize=12)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('FPR', fontsize=12)
    plt.ylabel('TPR', fontsize=12)
    plt.title('ROC Curve', fontsize=15)
    plt.legend(loc="lower right")
    # plt.show()
    plt.savefig('roc_auc_%s_new.pdf' % relation_results)
    return roc_auc


def drop_tables():
    
    datasets = ['darpa']
    density_measures = ['ari', 'geo', 'sus']
    select_methods = ['card', 'dense']

    for ds in datasets:
        for dm in density_measures:
            for sm in select_methods:
                relation_results = ds + '_results_' + dm + '_' + sm
                drop_table(db_conn, relation_results)

def main():
    global db_conn
    try:
        db_conn = connect_db()
        D_Cube_evaluation()
        drop_tables()
        close_db(db_conn)
        # print "D_Cube finished! Results are stored in %s_results and %s_parameters" % (relation, relation)
    except:
        print "Exception:", sys.exc_info()[0]
        if db_conn:
            close_db(db_conn)
        raise


# true_pos_kgroup={1: 231388, 2: 898930, 3: 1108322, 4: 1230333, 5: 1293539, 6: 1851962, 7: 2113542, 8: 2170426, 9: 2182055, 10: 2194575, 11: 2318562, 12: 2342026, 13: 2361569, 14: 2386026, 15: 2386071, 16: 2455885, 17: 2500564, 18: 2559567, 19: 2596721, 20: 2650007}
# false_pos_kgroup={1: 0, 2: 13, 3: 13, 4: 13, 5: 13, 6: 14808, 7: 14815, 8: 14815, 9: 14815, 10: 14815, 11: 14815, 12: 14820, 13: 23630, 14: 36311, 15: 39294, 16: 169486, 17: 328302, 18: 473890, 19: 599916, 20: 724878}

# plot_ROC_curve(true_pos_kgroup, false_pos_kgroup, pos_total, neg_total, pos_dup_factor, neg_dup_factor, '', 20)

if __name__ == "__main__":
    # args = sys.argv
    main()

# AUC: reference
# Datasets AirForce DARPA
# Elapsed Accuracy Elapsed Accuracy
# Time (sec) (AUC) Time (sec) (AUC)
# CPD [24] 413.2 0.854 105.0 0.926
# MAF [27] 486.6 0.912 102.4 0.514
# CrossSpot [19] 575.5 0.924 132.2 0.923
# M-Zoom [37] 27.7 0.975 22.7 0.923
# D-Cube 15.6 0.987 9.1 0.930

