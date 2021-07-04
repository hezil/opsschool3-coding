import json
import yaml


with open(r'C:\Users\HEZI LEVI\PycharmProjects\ops_assingment1\ppl_ages') as f:
    data = json.load(f)



def ppl_buckets(data):
    ppl_ages = data['ppl_ages']

    buckets = sorted(data['buckets'])

    a = []
    b = []
    c = []
    d = []

    for dict_key, dict_value in ppl_ages.items():
        # print(f'{dict_key} {dict_value}')
        if dict_value < buckets[0]:
            a.append(dict_key)

        elif dict_value >= buckets[0] and dict_value <= buckets[1]:
            b.append(dict_key)
        elif dict_value >= buckets[1] and dict_value <= buckets[2]:
            c.append(dict_key)
        elif dict_value >= buckets[2] and dict_value <= buckets[3]:
            d.append(dict_key)
        elif dict_value >= buckets[2] and dict_value <= buckets[3]:
            d.append(dict_key)

    data = dict(
        age11=list(a),
        age11_20=list(b),
        age20_25=list(c),
        age25_45=list(d),
    )

    with open(r'C:\Users\HEZI LEVI\PycharmProjects\ops_assingment1\ppl_in_ages_groups', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


if __name__ == "__main__":
    ppl_buckets(data)