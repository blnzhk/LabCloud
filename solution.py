from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = n / len(self.workers)

        # map
        mapped = []
        #default bug fix
        lastElementI = len(self.workers) - 1

        for i in xrange(0, lastElementI):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))
        #default bug fix
        mapped.append(self.workers[lastElementI].mymap(lastElementI * step, n))

        print 'Map finished: ', mapped

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        print (a, b)
        res = 0
        for i in xrange(a, b):
            if Solver.isPrime(i) : 
                res += 1
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

    @staticmethod
    def isPrime(n):
        if n == 2 or n == 3 :
            return True
        if n % 2 == 0 or n < 2 :
            return False
        for i in range(3, int(n**0.5) + 1, 2) :   # only odd numbers
                if n %i == 0 :
                    return False
        return True
        
        
        
