import csv

def GetStrArrFromColumn(col, csv_file):
  ans = []
  with open(csv_file,'r', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      #col列の要素を1つの文字列として扱い、コンマで区切った各要素を配列に入れる
      row[col] = row[col].split(',')
      ans.append(row[col])
  return ans

def GetNumArrFromColumn(col, csv_file, type="int"):
  ans = []
  with open(csv_file,'r', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      #col列の要素を1つの文字列として扱い、コンマで区切った各配列に入れる
      row[col] = row[col].split(',')
      items = []
      for item in row[col]:
        #itemが存在するときだけitemsに追加する(Noneの時は何もしない)
        if item:
          if type == "int":
            items.append(int(item))
          elif type == "float":
            items.append(float(item))
      ans.append(items)
  return ans

def GetNumFromColumn(col, csv_file, type="int"):
  ans = []
  with open(csv_file,'r', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if type == "int":
        ans.append(int(row[col]))
      elif type == "float":
        ans.append(float(row[col]))      
  return ans

# def main():
  # print(GetNumFromColumn("n_param","parameters.csv"))
  # print(GetNumFromColumn("x0","parameters.csv","float"))
  # print(GetNumFromColumn("v0","parameters.csv","float"))
  # print(GetNumArrFromColumn("gamma","parameters.csv","float"))
  # print(GetNumArrFromColumn("omega","parameters.csv","float"))
  # print(GetNumArrFromColumn("f0","parameters.csv","float"))
  # print(GetNumArrFromColumn("_omega","parameters.csv","float"))
  # print(GetStrArrFromColumn("label","parameters.csv"))
  # print(GetStrArrFromColumn("color","parameters.csv"))
  # print(GetNumFromColumn("n_step","parameters.csv"))
  # print(GetNumFromColumn("dt","parameters.csv","float"))
  # print(GetNumFromColumn("t0","parameters.csv","float"))

if __name__ == '__main__':
  main()