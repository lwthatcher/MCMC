
from burglar_alarm import alarm


def main():
    graph = alarm()
    p = graph.node_dict['A'].lookup_probability()
    print(p)

if __name__ == '__main__':
    main()