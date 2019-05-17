import os

import MySQLdb.cursors
import datetime
import redis
from _common.global_controller import GlobalController
from _common.utility import Utility


class DataBase:
    class MySql(object):

        def __init__(self, DB_CONNECT):
            self._db = None
            self.DB_CONNECT = DB_CONNECT

        def query_row(self, sql_query):
            if self._db is None or self._db.open == 0:
                self._db = MySQLdb.connect(host=self.DB_CONNECT['host'], user=self.DB_CONNECT['user'], passwd=self.DB_CONNECT['passwd'],
                                db=self.DB_CONNECT['db'], port=self.DB_CONNECT['port'], charset=self.DB_CONNECT['charset'],
                                cursorclass=self.DB_CONNECT['cursorclass'])

            try:
                cursors = self._db.cursor()
                cursors.execute(sql_query)
                self._db.commit()
                results = cursors.fetchall()
            except Exception, e:
                print e
                self._db.rollback()
            finally:
                self.sql_close()

            return results

        def query_column(self, sql_query):
            cursors = self._db.cursor()
            cursors.execute(sql_query)
            results = cursors.description
            return results

        def sql_run(self, sql_query, *args):
            try:
                sql_query_attrs = args
                sql_query = Utility.StringHandle().replace_in_turn(sql_query, sql_query_attrs)
                results = self.query_row(sql_query)
                results_return = []
                for result in results:
                    results_return.append(result)
            except Exception, e:
                print e

            return results_return

        def sql_backup(self, databases, backup_file_path, DB_CONNECT):
            try:
                if self._db is None or self._db.open == 0:
                    self._db = MySQLdb.connect(host=self.DB_CONNECT['host'], user=self.DB_CONNECT['user'],
                                               passwd=self.DB_CONNECT['passwd'],
                                               db=self.DB_CONNECT['db'], port=self.DB_CONNECT['port'],
                                               charset=self.DB_CONNECT['charset'],
                                               cursorclass=self.DB_CONNECT['cursorclass'])
                for db in databases:
                    file_name = '%s/%s.sql' % (backup_file_path, db)
                    result = os.system('cp %s/*.sql %s/backup/' % (backup_file_path, backup_file_path))
                    # if result != 0:

                    print 'backup file path is: ' + file_name
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    # db backup
                    os.system("mysqldump -h%s -u%s -p%s %s --default_character-set=%s > %s" % (
                        DB_CONNECT['host'], DB_CONNECT['user'], DB_CONNECT['passwd'], db, 'utf8', file_name))

                print 'The database backup success! %s' % datetime.time.strftime('%Y-%m-%d %H:%M:%S')
            except MySQLdb.Error, err:
                print err
            finally:
                self.sql_close()

        def sql_restore(self, databases, backup_file_path, DB_CONNECT):
            try:
                if self._db is None or self._db.open == 0:
                    self._db = MySQLdb.connect(host=self.DB_CONNECT['host'], user=self.DB_CONNECT['user'],
                                               passwd=self.DB_CONNECT['passwd'],
                                               db=self.DB_CONNECT['db'], port=self.DB_CONNECT['port'],
                                               charset=self.DB_CONNECT['charset'],
                                               cursorclass=self.DB_CONNECT['cursorclass'])
                for db in databases:
                    file_name = '%s/%s.sql' % (backup_file_path, db)
                    print 'backup file path is: ' + file_name
                    if os.path.exist(file_name):
                        print 'backup file %s not exist.' %(file_name)
                    # db restore
                    os.system(
                        "mysqldump -h%s -u%s -p%s %s --default_character-set=%s < %s" % (
                            DB_CONNECT['host'], DB_CONNECT['user'], DB_CONNECT['passwd'], db, 'utf8', file_name))

                print 'The database restore success! %s' % datetime.time.strftime('%Y-%m-%d %H:%M:%S')
            except MySQLdb.Error, err:
                print err
            finally:
                self.sql_close()

        def sql_close(self):
            if self._db:
                self._db.cursor().close()
                self._db.close()

    class Redis(object):

        def __init__(self):
            self._redis = GlobalController.REDIS_CONNECT

        def redis_connect(self):
            host = self._redis['host']
            port = self._redis['port']
            password = self._redis['auth']
            r = redis.Redis(host=host, port=port, password=password)
            return r


if __name__ == '__main__':
    m = DataBase
    r = m.MySql(DB_CONNECT=GlobalController.DB_CONNECT)
    databases = {'pdc'}
    home_path = os.environ['HOME']
    r.sql_backup(backup_file_path=home_path, databases=databases, DB_CONNECT=GlobalController.DB_CONNECT)
    print r.dbsize()
