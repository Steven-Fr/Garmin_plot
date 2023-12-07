import csv
import os
import fitparse
import pytz
import glob
allowed_fields = ['timestamp','position_lat','position_long', 'distance',
'enhanced_altitude', 'altitude','enhanced_speed',
                 'speed', 'heart_rate','temperature','cadence','fractional_cadence']
required_fields = ['timestamp']

UTC = pytz.UTC
CST = pytz.timezone('US/Pacific')

def main():
    cartella = 'file_fit_csv'
    files = glob.glob(os.path.join(cartella, '**', '*.fit'), recursive = True)
    print(files)
    fit_files = [file for file in files if file[-4:].lower()=='.fit']
    for file in fit_files:
        new_filename = file[:-4] + '.csv'
        if os.path.exists(new_filename):
            continue
        fitfile = fitparse.FitFile(file,data_processor=fitparse.StandardUnitsDataProcessor())
        
        print('converting %s' % file)
        write_fitfile_to_csv(fitfile, new_filename)
    print('finished conversions')


def write_fitfile_to_csv(fitfile, output_file='test_output.csv'):
    messages = fitfile.messages
    #raw data in messages in one line
    data = []
    for m in messages:
        skip=False
        if not hasattr(m, 'fields'):
            continue
        fields = m.fields
        #check for important data types
        mdata = {}
        for field in fields:
            #print(field) print varaibles
            if field.name in allowed_fields:
                if field.name=='timestamp':
                    mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                else:
                    mdata[field.name] = field.value    
        for rf in required_fields:
            if rf not in mdata:
                skip=True
                
        if not skip:
            data.append(mdata)       
    #write to csv
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(allowed_fields)

        for entry in data:
            line_file=[]
            for k in allowed_fields:
                data_var= str(entry.get(k,""))
                #print(entry," ", k," " ,data_var)
                line_file.append(data_var)
            writer.writerow(line_file)


if __name__=='__main__':
    main()