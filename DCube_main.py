from DCube_params import *
from DCube_sql import *
import sys
import numpy as np

db_conn = None


def D_Cube():
    drop_and_copy_table(db_conn, relation, relation+"_copy", "*")
    drop_and_copy_table(db_conn, relation, relation+"_results", "*", copy_data=False)
    drop_and_create_table(db_conn, relation+"_parameters", "block integer, density numeric, row_count integer")
    for da in dimension_attributes:
        drop_and_copy_table(db_conn, relation, relation+"_"+da+"_set", "distinct "+da)
    for itr in range(1, 1+k):
        if DEBUG:
            print "iteration:", itr
        try:
            if measure_attribute == "":
                relation_mass = float(get_first_res(db_conn, "select count(*) from %s" % relation))
                if relation_mass == 0.0:
                    print "relation already empty"
                    return
            else:
                relation_mass = float(get_first_res(db_conn, "select sum(%s) from %s" % (measure_attribute, relation)))
        except:
            print "relation already empty"
            return
        max_density = find_single_block(relation_mass)

        """
        drop_and_copy_table(db_conn, relation, "%s_tuple_to_remove" % relation, "*")
        for da in dimension_attributes:
            exec_sql(db_conn, "delete from %s_tuple_to_remove a where not exists "
                              "(select * from %s_%s_res_block_set b where a.%s=b.%s)" %
                     (relation, relation, da, da, da))
        sql = "delete from %s a using %s_tuple_to_remove b where " % (relation, relation)
        for da in dimension_attributes:
            sql += "a.%s=b.%s AND " % (da, da)
        sql = sql[:-5]
        exec_sql(db_conn, sql)
        drop_table(db_conn, "%s_tuple_to_remove" % relation)
        """

        # improve efficiency
        exec_sql(db_conn, "alter table %s add column _to_remove smallint default 1" % relation)
        for da in dimension_attributes:
            update(db_conn, relation, "_to_remove = 0 where not exists "
                                      "(select * from %s_%s_res_block_set b where %s.%s=b.%s)" %
                   (relation, da, relation, da, da))
        exec_sql(db_conn, "delete from %s where _to_remove = 1" % relation)
        exec_sql(db_conn, "alter table %s drop column _to_remove" % relation)

        for da in dimension_attributes:
            drop_and_copy_table(db_conn, relation, relation+"_"+da+"_set", "distinct "+da)

        drop_and_copy_table(db_conn, "%s_copy" % relation, "%s_res_to_add" % relation, "*")
        for da in dimension_attributes:
            exec_sql(db_conn, "delete from %s_res_to_add a where not exists "
                              "(select * from %s_%s_res_block_set b where a.%s=b.%s)" %
                     (relation, relation, da, da, da))
        exec_sql(db_conn, "insert into %s_results select * from %s_res_to_add" % (relation, relation))
        block_cnt = int(get_first_res(db_conn, "select count(*) from %s_res_to_add" % relation))
        drop_table(db_conn, "%s_res_to_add" % relation)
        insert(db_conn, relation+"_parameters", "%d, %.8f, %d" % (itr, max_density, block_cnt))
        print "block %d: density: %.8f count: %d" % (itr, max_density, block_cnt)


def update_block_set_and_block_card_list():
    drop_and_create_table(db_conn, relation+"_block_card_list", "attribute varchar(%d), card integer" %
                          max_len_of_attributes)
    cnt_block_set = 0
    for da in dimension_attributes:
        drop_table(db_conn, relation+"_"+da+"_block_set")
        exec_sql(db_conn, "create table %s_%s_block_set as (select distinct(%s) from %s_block)" %
                 (relation, da, da, relation))
        cur_card = int(get_first_res(db_conn, "select count(%s) from %s_%s_block_set" % (da, relation, da)))
        cnt_block_set += cur_card
        insert(db_conn, relation + "_block_card_list", "'%s', %d" % (da, cur_card))
    return cnt_block_set


def find_single_block(relation_mass):
    drop_and_copy_table(db_conn, relation, relation+"_block", "*")
    block_mass = relation_mass
    cnt_block_set = 0
    drop_and_create_table(db_conn, relation+"_block_card_list", "attribute varchar(%d), card integer" %
                          max_len_of_attributes)
    drop_and_create_table(db_conn, relation+"_card_list", "attribute varchar(%d), card integer" %
                          max_len_of_attributes)
    for da in dimension_attributes:
        drop_and_copy_table(db_conn, relation+"_"+da+"_set", relation+"_"+da+"_block_set", "*")
        cur_card = int(get_first_res(db_conn, "select count(%s) from %s_%s_block_set" % (da, relation, da)))
        cnt_block_set += cur_card
        insert(db_conn, relation+"_block_card_list", "'%s', %d" % (da, cur_card))
        insert(db_conn, relation+"_card_list", "'%s', %d" % (da, cur_card))

    # max_density = calc_density(block_mass, relation_mass)
    max_density = 0.0
    r, best_r = 1, 1
    for da in dimension_attributes:
        # drop_and_copy_table(db_conn, relation+"_"+da+"_set", relation+"_"+da+"_order", "*", copy_data=False)
        # exec_sql(db_conn, "alter table %s_%s_order add column orders integer" % (relation, da))
        drop_and_copy_table(db_conn, relation+"_"+da+"_set", relation+"_"+da + "_order", "*")
        exec_sql(db_conn, "alter table %s_%s_order add column orders integer default %d" %
                 (relation, da, cnt_block_set+2))

    while cnt_block_set > 0:
        # bug fix
        max_density = calc_density(block_mass, relation_mass)
        for da in dimension_attributes:
            drop_table(db_conn, "%s_%s_mass_set" % (relation, da))
            if measure_attribute == "":
                exec_sql(db_conn, "create table %s_%s_mass_set as (select %s, count(*) as mass "
                                  "from %s_block group by %s)" % (relation, da, da, relation, da))
            else:
                exec_sql(db_conn, "create table %s_%s_mass_set as (select %s, sum(%s) as mass "
                                  "from %s_block group by %s)" % (relation, da, da, measure_attribute, relation, da))
        dimension = select_dimension(block_mass, relation_mass)
        cur_card = int(get_first_res(db_conn, "select count(%s) from %s_%s_block_set" %
                                     (dimension, relation, dimension)))
        drop_table(db_conn, "%s_%s_remove_set" % (relation, dimension))
        exec_sql(db_conn, "drop index if exists %s_%s_remove_set_index" % (relation, dimension))
        # exec_sql(db_conn, "create table %s_%s_remove_set as "
        #         "(select a.%s, b.mass from %s_%s_block_set a, %s_%s_mass_set b "
        #         "where a.%s=b.%s and b.mass <= %.16f / (%d * 1.0) order by b.mass)" %
        #          (relation, dimension, dimension, relation, dimension, relation,
        #           dimension, dimension, dimension, block_mass, cur_card))
        exec_sql(db_conn, "create table %s_%s_remove_set as (select %s, mass, rank() over(order by mass, %s) as idx"
                          " from %s_%s_mass_set where mass <= %.16f / (%d * 1.0) order by mass, %s)" %
                 (relation, dimension, dimension, dimension, relation, dimension, block_mass, cur_card, dimension))
        exec_sql(db_conn, "create index %s_%s_remove_set_index on %s_%s_remove_set(idx)" %
                 (relation, dimension, relation, dimension))
        removed_size = int(get_first_res(db_conn, "select count(%s) from %s_%s_remove_set" %
                                         (dimension, relation, dimension)))
        # TODO: try iterate using cursor
        if DEBUG:
            print "removed_size:", removed_size
        for i in range(1, removed_size+1):
            cur = db_conn.cursor()
            cur.execute("select %s, mass from %s_%s_remove_set where idx=%d" % (dimension, relation, dimension, i))
            a, mass_a = cur.fetchone()[0:2]
            mass_a = float(mass_a)
            db_conn.commit()
            sql = cur.mogrify("delete from %s_%s_block_set where %s=%%s" % (relation, dimension, dimension), (a, ))
            cur.execute(sql)
            db_conn.commit()
            block_mass -= mass_a
            cur.close()

            update(db_conn, "%s_block_card_list" % relation, "card = card - 1 where attribute='%s'" % dimension)
            tmp_density = calc_density(block_mass, relation_mass)
            cur = db_conn.cursor()
            # sql = cur.mogrify("insert into %s_%s_order(%s, orders) values(%%s, %d)" %
            #                   (relation, dimension, dimension, r), (a,))
            sql = cur.mogrify("update %s_%s_order set orders=%d where %s=%%s" %
                              (relation, dimension, r, dimension), (a,))
            cur.execute(sql)
            db_conn.commit()
            cur.close()

            r += 1
            if tmp_density > max_density:
                max_density = tmp_density
                best_r = r
        if DEBUG:
            print "best_r", best_r
        exec_sql(db_conn, "delete from %s_block a where exists (select * from %s_%s_remove_set b "
                          "where a.%s=b.%s)" % (relation, relation, dimension, dimension, dimension))
        cnt_block_set = update_block_set_and_block_card_list()

    for da in dimension_attributes:
        drop_table(db_conn, "%s_%s_res_block_set" % (relation, da))
        exec_sql(db_conn, "select %s into %s_%s_res_block_set from %s_%s_order where orders >= %d" %
                 (da, relation, da, relation, da, best_r))
    return max_density


def calc_density(block_mass, relation_mass):
    if density_measure == "ari":
        cur_density = block_mass * len(dimension_attributes) / \
                      float(get_first_res(db_conn, "select sum(card) from %s_block_card_list" % relation))
        return cur_density
    elif density_measure == "geo":
        cur_density = 1.0
        for da in dimension_attributes:
            cur_density *= float(get_first_res(db_conn, "select card from %s_block_card_list where attribute='%s'" %
                                               (relation, da)))
        if cur_density == 0.0:
            return cur_density
        cur_density = block_mass / (cur_density ** (1.0 / len(dimension_attributes)))
        return cur_density
    elif density_measure == "sus":
        if block_mass == 0.0:
            return 0.0
        cur_density = block_mass * (np.log(block_mass * 1.0 / relation_mass) - 1)
        prod = 1.0
        for da in dimension_attributes:
            prod *= float(get_first_res(db_conn,
                                    "select card from %s_block_card_list where attribute='%s'" % (relation, da))) / \
                    float(get_first_res(db_conn, "select card from %s_card_list where attribute='%s'" % (relation, da)))
        cur_density = cur_density + relation_mass * prod - block_mass * np.log(prod)
        return cur_density
    else:
        print "invalid density measurement"
        exit(-1)


def select_dimension(block_mass, relation_mass):
    if dimension_selection == "card":
        max_card = 0
        dimension = ""
        for da in dimension_attributes:
            cur_card = int(get_first_res(db_conn, "select count(%s) from %s_%s_block_set" % (da, relation, da)))
            if cur_card > max_card:
                max_card = cur_card
                dimension = da
            if DEBUG:
                print "dimension:", da, "card:", cur_card, get_first_res(db_conn,
                                                                         "select count(*) from %s_%s_mass_set" %
                                                                         (relation, da))
        if DEBUG:
            print "selected dimension:", dimension
        return dimension
    elif dimension_selection == "dense":
        max_density = float("-inf")
        dimension = ""
        for da in dimension_attributes:
            cur_card = int(get_first_res(db_conn, "select card from %s_block_card_list where attribute='%s'" %
                                         (relation, da)))
            if cur_card > 0:
                drop_table(db_conn, relation+"_"+da+"_remove_set")
                # exec_sql(db_conn, "create table %s_%s_remove_set as "
                #                   "(select a.%s from %s_%s_block_set a, %s_%s_mass_set b "
                #                   "where a.%s = b.%s and b.mass <= %.16f / (%d * 1.0))"
                #         % (relation, da, da, relation, da, relation, da, da, da, block_mass, cur_card))
                exec_sql(db_conn, "create table %s_%s_remove_set as (select %s from %s_%s_mass_set "
                                  "where mass <= %.16f / (%d * 1.0))"
                        % (relation, da, da, relation, da, block_mass, cur_card))

                tmp_block_mass = block_mass - float(get_first_res(db_conn,
                                    "select sum(mass) from %s_%s_mass_set a where exists "
                                    "(select * from %s_%s_remove_set b where a.%s=b.%s)" %
                                    (relation, da, relation, da, da, da)) or 0.0)
                removed_size = int(get_first_res(db_conn, "select count(*) from %s_%s_remove_set" % (relation, da)))
                update(db_conn, relation+"_block_card_list", "card = card - %d where attribute='%s'" % (removed_size, da))
                tmp_density = calc_density(tmp_block_mass, relation_mass)
                update(db_conn, relation+"_block_card_list", "card = card + %d where attribute='%s'" % (removed_size, da))
                if tmp_density > max_density:
                    max_density = tmp_density
                    dimension = da
                if DEBUG:
                    print "dimension:", da, "card:", cur_card, get_first_res(db_conn,
                                                              "select count(*) from %s_%s_mass_set" %
                                                              (relation, da)), "density:", tmp_density
        if DEBUG:
            print "selected dimension:", dimension
        return dimension


def drop_tables():
    global_tables = ["_block", "_block_card_list", "_card_list", "_res_to_add", "_tuple_to_remove"]
    da_tables = ["_block_set", "_mass_set", "_order", "_remove_set", "_res_block_set", "_set"]
    for tb in global_tables:
        drop_table(db_conn, relation+tb)
    for da in dimension_attributes:
        for tb in da_tables:
            drop_table(db_conn, relation+"_"+da+tb)


def main():
    global db_conn
    try:
        db_conn = connect_db()
        #drop_tables()
        #return
        D_Cube()
        close_db(db_conn)
    except:
        print "Exception:", sys.exc_info()[0]
        if db_conn:
            close_db(db_conn)
        raise


if __name__ == "__main__":
    main()
