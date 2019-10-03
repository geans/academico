from random import randint

# Order:
#   Data_Creation    Duration   Priority

f = open('10.input', 'w')
for i in range(0,10):
    f.write(str(randint(0,10))+' '+str(randint(0,10))+' '+str(randint(0,10))+'\n')
f.close()

f = open('20.input', 'w')
for i in range(0,20):
    f.write(str(randint(0,10))+' '+str(randint(0,10))+' '+str(randint(0,10))+'\n')
f.close()

f = open('30.input', 'w')
for i in range(0,30):
    f.write(str(randint(0,10))+' '+str(randint(0,10))+' '+str(randint(0,10))+'\n')
f.close()