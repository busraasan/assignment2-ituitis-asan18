from hashlib import sha256

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

myhash = "407a7714ed0e531d4d4e2a3adc8f882630aa9ce059de02e1a1f8351f09c1bd31"
comments = []

while True:
    comment = input('Enter your comment: ')
    password = input('Enter your password: ')
    hash1 = create_hash(password)

    j = 1
    if hash1 == myhash:
        comments.append(comment)
        print("Previously entered comments: ")
        for comm in comments:
            print("%(j)d." % {"j": j} + comments[j-1])
            j += 1
    else:
        print("I'm sorry I can't let you do that.")
