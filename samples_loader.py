import pickle


def load_samples(file_name):
    with open(file_name, 'rb') as f:
        samples = pickle.load(f)
    return samples
