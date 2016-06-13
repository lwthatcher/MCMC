import json

file_name = 'alarm-expected-orig.json'
with open(file_name, 'r') as f:
    d = json.load(f)

print('P(B=t):', d['b_B'])
print('P(E=t):', d['b_E'])
print('P(A=t | B=t, E=t):', d['b_A_11'])
print('P(A=t | B=t, E=f):', d['b_A_10'])
print('P(A=t | B=f, E=t):', d['b_A_01'])
print('P(A=t | B=f, E=f):', d['b_A_00'])
print('P(J=t | A=t):', d['b_J_1'])
print('P(J=t | A=f):', d['b_J_0'])
print('P(M=t | A=t):', d['b_M_1'])
print('P(M=t | A=f):', d['b_M_0'])
