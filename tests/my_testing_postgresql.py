__author__ = 'mlatief'
import subprocess
import os, signal
import pg8000
from time import sleep
from datetime import datetime
import testing.postgresql
from contextlib import closing
from testing.postgresql import get_unused_port


class MyPostgresql(testing.postgresql.Postgresql):
    def start(self):
        if self.pid:
            return  # already started

        if self.port is None:
            self.port = get_unused_port()

        logger = open(os.path.join(self.base_dir, 'tmp', 'postgresql.log'), 'wt')

        # Replace fork with subprocess.Popen
        # pid = os.fork()
        #p = multiprocessing.Process(target=run_postgres, args=(logger, self.postgres, self.port, self.base_dir, self.postgres_args))
        #p.start()
        #p.join()

        args = [self.postgres,
                 '-p', str(self.port),
                 '-D', os.path.join(self.base_dir, 'data'),
                 '-k', os.path.join(self.base_dir, 'tmp')]
        args.extend((self.postgres_args.split()))
        print "Starting .. ", args
        p = subprocess.Popen(args, stdout=logger.fileno(), stderr=logger.fileno())
        self.pid = p.pid
        self.p = p
        print "... started {}".format(p.pid)
        logger.close()

        exec_at = datetime.now()
        while True:
            r = p.poll()
            if r is not None:
                raise RuntimeError("*** failed to launch postgres ***\n" + self.read_log())

            if self.is_connection_available():
                break

            if (datetime.now() - exec_at).seconds > 10.0:
                raise RuntimeError("*** failed to launch postgres (timeout) ***\n" + self.read_log())

            sleep(0.1)

        # create test database
        with closing(pg8000.connect(**self.dsn(database='postgres'))) as conn:
            conn.autocommit = True
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT COUNT(*) FROM pg_database WHERE datname='test'")
                if cursor.fetchone()[0] <= 0:
                    cursor.execute('CREATE DATABASE test')

    def terminate(self, _signal=signal.SIGINT):
        if self.p is None:
            return  # not started

        if self._owner_pid != os.getpid():
            return  # could not stop in child process

        try:
            #os.kill(self.pid, _signal)
            print "Terminating postgres subprocess..."
            self.p.terminate()
            killed_at = datetime.now()
            while (self.p.poll()):
                if (datetime.now() - killed_at).seconds > 10.0:
                    self.p.kill()
                    raise RuntimeError("*** failed to shutdown postgres (timeout) ***\n" + self.read_log())

                sleep(0.1)
        except OSError:
            pass

        print "... postgres subprocess terminated!"
        self.pid = None