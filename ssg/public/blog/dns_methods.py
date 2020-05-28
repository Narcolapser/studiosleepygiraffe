import struct

example_request  = b'Bx\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'
example_request2 = b'\xb2"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x1c\x00\x01'

example_response = b'Bx\x81\x80\x00\x01\x00\x04\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x01+\x00\x04\xd8\xef u\xc0\x0c\x00\x01\x00\x01\x00\x00\x01+\x00\x04\xd8\xef$u\xc0\x0c\x00\x01\x00\x01\x00\x00\x01+\x00\x04\xd8\xef&u\xc0\x0c\x00\x01\x00\x01\x00\x00\x01+\x00\x04\xd8\xef"u'

qtypes_answer = {'A':1,'NS':2,'MD':3,'MF':4,'CNAME':5,'SOA':6,'MB':7,
                 'MG':8,'MR':9,'NULL':10,'WKS':11,'PTR':12,'HINFO':13,
                 'MINFO':14,'MX':15,'TXT':16}

qtypes_question = {qtypes_answer[q]:q for q in qtypes_answer}

qclasses_answer = {'IN':1,'CS':2,'CH':3,'HS':4}

qclasses_question = {qclasses_answer[q]:q for q in qclasses_answer}


def convert_2_bytes_to_int(upper,lower):
    # On a more professional level this should be done with python's struct
    # library, but I'm breaking it out here to make more visible what is
    # happening. We have two bytes that we want to convert to an ingeter,
    # the simplest way to do this is to just simply byte shift the first one
    # and then add them together. This command moves the contents of the byte
    # over by 8 so that the lower byte can fit in
    upper = upper << 8
    result = upper + lower
    return result


def convert_bytes_to_int(byte_list):
    # I mentioned python's struct method above. I'm going to use that here since
    # I need to also have a method of converting larger lists of bytes into 
    # integer values. More information can be found in the python documentation:
    # https://docs.python.org/3/library/struct.html
    # But I'll give you a breif introduction here.
    
    return struct.unpack('!I',byte_list)[0]

def convert_int_to_bytes(integer, byte_count = 2):
    # When bytes does its conversion it expects a list of integers integers
    # between 0 and 256. Try typing "bytes([500])" into the interpreter and
    # you will be informed of such. So we need to do some work on this
    # unknown integer to get it into the correct shape.
    result = b''
    while integer:
        # Pop off the smallest integer value:
        small = integer % 256

        # Next we push it onto the result pushing smaller values down.
        result = bytes([small]) + result

        # Knock that byte off, if it's the last one this will return a
        # zero which will stop the while loop.
        integer = int(integer/256)

    # We will probably be converting a lot of single byte integers who need
    # to be two bytes wide, like for qclass and qtype. So we need to have
    # a step here to pad out the value in such a case:
    while len(result) < byte_count:
        # Add empty bytes to pad.
        result = b'\x00' + result

    return result


def process_header(val):
    # The objective here is to process out the parts of the dns header

    # DNS Headers are a fixed 12 bytes.
    if len(val) != 12:
        return False

    # TODO: Document this step
    request_id = convert_2_bytes_to_int(val[0],val[1])

    # The next part is complicated. The next two bytes represent 8 fields, 5
    # of which are 1 bit. fortunately python's string formater provides a
    # method for converting bytes into a binary string:
    bits = '{0:08b}{1:08b}'.format(val[2],val[3])

    # This is a little easier to work with, from here it breaks out like so:
    #                                1  1  1  1  1  1
    #  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    qr     = bits[0]
    opcode = bits[1:5]
    aa     = bits[5]
    tc     = bits[6]
    rd     = bits[7]
    ra     = bits[8]
    z      = bits[9:12] #this is always zero actually.
    rcode  = bits[12:]

    # Finally we repeat the trick for ID to get the counts of the various
    # questions and responses.

    # QDCOUNT or question count
    qdcount = convert_2_bytes_to_int(val[4], val[5])

    # ANCOUNT or answer count
    ancount = convert_2_bytes_to_int(val[6], val[7])

    # NSCOUNT or NameServer count
    nscount = convert_2_bytes_to_int(val[8], val[9])

    # ARCOUNT or Additional Records count
    arcount = convert_2_bytes_to_int(val[10],val[11])
    return request_id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount


def process_questions(req, qdcount):
    # This is a little more tricky since the size of the structure can vary.
    start = 12
    questions = []
    for i in range(qdcount):
        # We don't know how many labels there are, so we will loop while the
        # Size of the label is greater than 0
        size = req[start]
        parts = []
        while size:
            # Move start forward one to get past the size byte.
            start += 1

            # Using start and size, grab the label and convert to a string
            parts.append(req[start:start+size].decode('utf-8'))

            # Move start to the begining of the next label
            start += size

            # Extract the next label's size.
            size = req[start]

        # Move the starting pointer past the zero byte that signalled the
        # end of the labels above.
        start += 1

        # Qtype comes next and it is always 2 bytes
        qtype_raw = req[start:start+2]
        qtype_int = convert_2_bytes_to_int(qtype_raw[0], qtype_raw[1])
        qtype = qtypes_question[qtype_int]

        # Advance the pointer past Qtype
        start += 2

        # Followed by Qclass which is also 2 bytes
        qclass_raw = req[start:start+2]
        qclass_int = convert_2_bytes_to_int(qclass_raw[0], qclass_raw[1])
        qclass = qclasses_question[qclass_int]
        start += 2
        
        questions.append(('.'.join(parts),qtype,qclass))
    return questions,start


def create_questions(urls):
    questions = b''
    for url in urls:
        # Split the url into it's components to follow the DNS spec.
        for label in url.split('.'):
            # First add a byte with the length of the label.
            questions += bytes([len(label)])

            # Next add the label itself.
            questions += label.encode('utf-8')

        # Add an empty byte to indicate the end of the labels.
        questions += b'\x00'
        
        # Next we add the type, for now we are only concerned with
        # IPv4 recoreds.
        questions += bytes([0,qtypes_answer['A']])

        # Finally add the class, here we are also only concerned
        # about internet class records.
        questions += bytes([0,qclasses_answer['IN']])

    return questions


def create_header(request_id = 0,
                  qr = 0,
                  opcode = 0,
                  aa = 0,
                  tc = 0,
                  rd = 0,
                  ra = 0,
                  z = 0,
                  rcode = 0,
                  qdcount = 0,
                  ancount = 0,
                  nscount = 0,
                  arcount = 0):
    # I am making all the arguments optional since many of them will be zero
    # most of the time. This way you only need to send the arguments that
    # are actually interesting.

    header = b''

    # First the request id:
    header += convert_int_to_bytes(request_id)

    # Next all the flags, for reference again:
    #                                1  1  1  1  1  1
    #  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    bits  = '{0:01b}'.format(qr)
    bits += '{0:04b}'.format(opcode)
    bits += '{0:01b}'.format(aa)
    bits += '{0:01b}'.format(tc)
    bits += '{0:01b}'.format(rd)    
    bits += '{0:01b}'.format(ra)
    bits += '{0:03b}'.format(z)
    bits += '{0:04b}'.format(rcode)

    # Now convert the string of bits into an int:
    flags = int(bits, 2)

    # Lastly convert that into bytes and push it onto the header
    header += convert_int_to_bytes(flags)

    # Now the counts:
    header += convert_int_to_bytes(qdcount)
    header += convert_int_to_bytes(ancount)
    header += convert_int_to_bytes(nscount)
    header += convert_int_to_bytes(arcount)

    return header

def process_resource_record(response,record_start):
    #                                1  1  1  1  1  1
    #  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|                                               |
    #/                                               /
    #/                      NAME                     /
    #|                                               |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|                      TYPE                     |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|                     CLASS                     |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|                      TTL                      |
    #|                                               |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    #|                   RDLENGTH                    |
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    #/                     RDATA                     /
    #/                                               /
    #+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    
    # In most cases we will be dealing with the DNS protocol's compression 
    # scheme here. The way it works is instead of putting in a name, done the
    # same was as the question record above, it instead puts a pointer to the
    # question record above. The way to spot compression is the first two bits
    # of the first byte are 11. This is because labels are limited to 63 
    # characters long, so the top two bits are used for other purposes. 
    # Currently compression is the only purpose.
    bits = '{0:08b}{1:08b}'.format(response[record_start],response[record_start+1])
    if bits[0:2] == '11':
        # We now need to get the offset. This isn't the best route but it's easy
        # to understand. Just some quick string manipulation:
        offset_bits = '00' + bits[2:]
        offset = int(offset_bits,2)
        label_pointer = offset
    else:
        # If there is no compression, the label starts where the record does.
        label_pointer = record_start
    
    
    size = response[label_pointer]
    parts = []
    while size:
        # Move start forward one to get past the size byte.
        label_pointer += 1

        # Using start and size, grab the label and convert to a string
        parts.append(response[label_pointer:label_pointer+size].decode('utf-8'))

        # Move start to the begining of the next label
        label_pointer += size

        # Extract the next label's size.
        size = response[label_pointer]
    
    # Finally move the record pointer past the name to get the rest of the content
    if bits[0:2] == '11':
        pointer = record_start + 2
    else:
        pointer = record_start + label_pointer + 1 #don't foget the last byte.
    
    # Next is type, two bytes:
    raw_type = convert_2_bytes_to_int(response[pointer], response[pointer+1])
    print(raw_type)
    pointer += 2
    
    # Next is class, two bytes:
    raw_class = convert_2_bytes_to_int(response[pointer], response[pointer+1])
    print(raw_class)
    pointer += 2
    
    # Next is time to live, in seconds. This specifies how long you should cache
    # this record. i.e. How often you need to request the record. A time of 0
    # seconds means it should not be cached.
    ttl = convert_bytes_to_int(response[pointer:pointer+4])
    print(ttl)
    pointer += 4
    
    # Penultimately we have the lengh of the data payload. Two bytes.
    rdlength = convert_2_bytes_to_int(response[pointer], response[pointer+1])
    print(rdlength)
    pointer += 2
    
    # Lastly the payload we are actually looking for. rdlength bytes.
    data = response[pointer:pointer+rdlength]
    
    # If you were to look at this now it would not be what you would expect.
    # We are used to seeing '192.168.0.1' but that IP address actually looks
    # like this: 11000000101010000000000000000001
    # So in order to get this to look like we are used we need to do a little
    # bit of formatting.
    address_ints = [str(int(datum)) for datum in data]
    address = '.'.join(address_ints)
    print(address)
    

#print(process_questions(example_response,1))
process_resource_record(example_response,32)

def create_resource_record(record):
    pass

