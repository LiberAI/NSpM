from tqdm import tqdm
import argparse

def eliminator(input_file, output_file,threshold):
        lines = open(input_file,'r').readlines()
        print(len(lines))
        accum = []
        nspm_ready = open(output_file,'w')
        for line in tqdm(lines):
                values = line.split(";")
                if(int(values[-1])>int(threshold)):
                        accum.append(";".join(values[:-1])+"\n")
                        nspm_ready.write(accum[-1])
        nspm_ready.close()


if __name__ == "__main__":
        """
        Section to parse the command line arguments.
        """
        parser = argparse.ArgumentParser()
        requiredNamed = parser.add_argument_group('Required Arguments')

        requiredNamed.add_argument('--input', dest='input', metavar='input',
                                                                help='Input file name ', required=True)
        requiredNamed.add_argument(
                '--output_file', dest='output', metavar='output', help='Output file name', required=True)
        requiredNamed.add_argument(
                '--threshold', dest='threshold', metavar='threshold', help='threshold', required=True)
        args = parser.parse_args()
        input_file = args.input
        output_file = args.output
        threshold = args.threshold
        eliminator(input_file=input_file, output_file=output_file,threshold=threshold)
        pass

        