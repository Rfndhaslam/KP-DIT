// visit_website.tag
https://see.labs.telkomuniversity.ac.id/praktikum/index.php/home

// Tunggu sampai halaman sepenuhnya dimuat
wait 3

// Isi field username (misalnya field dengan id "username")
type //*[@id="formID"]/div/div[2]/div[1]/input as ---

// isi password
type //*[@id="formID"]/div/div[2]/div[2]/input as ---

// select 
select //*[@id="formID"]/div/div[2]/div[3]/select as Asisten

// klik sign in
click //*[@id="formID"]/div/div[2]/div[5]/button

// Tunggu sampai halaman sepenuhnya dimuat
wait 3

// klik hasil input
click /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// Tunggu sampai halaman sepenuhnya dimuat
wait 3

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 1

// klik view kel 1
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check0.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 1

// klik view kel 2
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[7]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check1.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 1

// klik view kel 3
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[11]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check2.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 1

// klik view kel 4
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[16]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check3.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 2

// klik view kel 1
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check4.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 2

// klik view kel 2
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[7]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check5.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 2

// klik view kel 3
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[11]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check6.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 2

// klik view kel 4
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[16]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check7.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 3

// klik view kel 1
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check8.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 3

// klik view kel 2
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[7]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check9.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 3

// klik view kel 3
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[11]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check10.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 3

// klik view kel 4
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[16]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check11.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 4

// klik view kel 1
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check12.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 4

// klik view kel 2
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[7]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check13.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 4

// klik view kel 3
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[11]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check14.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// select modul
select  /html/body/div[2]/div[2]/div/div[2]/form/div/div[2]/select  as  Modul 4

// klik view kel 4
click   /html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[16]/td[5]/input[4]

// ekstrak table
table   /html/body/div[2]/div[2]/div/div[2]/form/table  to  check15.csv

//klik hasil input
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[18]/a

// logout
click   /html/body/div[2]/div[2]/div/div[1]/div/ul/li[30]/a