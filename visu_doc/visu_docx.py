import docx


def creat_doc_data(N,a,d,q) :
    '''
    creation a docx doc --> add just the data to the problem
    '''
    doc = docx.Document() 
  
    doc.add_heading('One machine sequencing problem', 0)
    doc.add_paragraph('Presentation of the data : ')

    data = []

    for i in range(len(N)) :
        job = "Job "+str(N[i])
        row = (job , a[i] , d[i] , q[i])
        data.append(row)
    
    data = tuple(data)

    table = doc.add_table(rows=1, cols=4)
    row = table.rows[0].cells 
    row[0].text = 'Job'
    row[1].text = 'starting_time'
    row[2].text = 'processing_time'
    row[3].text = 'queuing_time'

    for n,start , process,queuing in data: 
  
    
        row = table.add_row().cells 
        row[0].text = n 
        row[1].text = str(start)
        row[2].text = str(process)
        row[3].text = str(queuing)

    table.style = 'Colorful List'

    return doc

def doc_add_shrage_sol(N,a,d,q):

    plt.savefig('client_report/test.png')

    document = creat_doc_data(N,a,d,q)
    document.add_heading('Report',0)
    document.add_picture('test.png', width=Inches(1.25))

def doc_add_mip_sol(doc):
    pass

def doc_compute_save(N,a,d,q,name="test.docx"):
    pass






if __name__ == "__main__" :

    N = list(range(1,8))
    a = [10,13,11,20,30,0,30]
    d = [5,6,7,4,3,6,2]
    q = [7,26,24,21,8,17,0]

    pass