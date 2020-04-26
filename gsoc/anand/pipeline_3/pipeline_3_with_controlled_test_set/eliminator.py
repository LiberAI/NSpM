from tqdm import tqdm
import argparse

def eliminator():
        """
        The function remove the templates which are considered as less popular 
        based on the proposed ranking mechanism, the input files should be pre processed
        and a TRUE or FALSE should be added as the last column. 

        This function just removes the entries with FALSE as the last entry in a row 
        and create a file name new_train.csv to be used for futher purposes.
        """
        lines = open(location,'r').readlines()
        print(len(lines))
        accum = []
        nspm_ready = open("new_train.csv",'w')
        for line in tqdm(lines):
                values = line.split(",")
                if(len(values)<8):
                        print("Input file is of wrong format, please add the corect bolean values as the last column entry to use this function")
                print(values[-1])
                if(values[-1]=="TRUE\n"):
                        accum.append(";".join(values[:-2])+"\n")
                        nspm_ready.write(accum[-1])
        nspm_ready.close()

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        requiredNamed = parser.add_argument_group('Required Arguments')

        requiredNamed.add_argument('--location', dest='location', metavar='location',
                                                                help='location of the file to be pruned.', required=True)
        args = parser.parse_args()
        location = args.location
        eliminator(location)
        pass


        