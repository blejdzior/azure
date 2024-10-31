


## Ćwiczenie 1

### 1. Tworzenie SQL Database
   Na ekranie głównym portalu Azure wybierz "Utwórz zasób"
   #### a. Tworzenie grupy zasobów
   Wybierz istniejącą grupę zasobów z listy lub utwórz nową tak jak pokazane na poniższym zrzucie ekranu.
   ![image](https://github.com/user-attachments/assets/dbe6a146-a25d-462a-8114-d887b81e3b5a)

   #### b. Nazwa bazy danych i serwer
   Wpisz nazwę tworzonej bazy danych oraz wybierz istniejący serwer z listy lub stwórz nowy.
   ![image](https://github.com/user-attachments/assets/c316a6ad-7233-4fed-80ff-6b74447f9715)

   ##### Tworzenie i konfiguracja nowego serwera
   Wpisz nazwę serwera, wybierz odpowiednie położenie serwera, następnie skonfiguruj metodę autoryzacji dostępu do bazy danych, w tym przypadku wybrana została autoryzacja SQL
   ![image](https://github.com/user-attachments/assets/459cda87-4e63-4a39-ba49-7fb796d93ccf)

   #### c. Skonfiguruj plan cenowy bazy danych
   Wybierz poziom usług oraz poziom sprzętowy.
   ![image](https://github.com/user-attachments/assets/499699c7-2e5b-4293-9f34-19d815727cba)

   W tym kroku warto zwrócić uwagę na przewidywane koszty korzystania z bazy danych pokazane po prawej stronie ekranu.
   ![image](https://github.com/user-attachments/assets/97a85764-c621-4098-86ef-ae9cc985ff3d)

   #### d. Ustawienia kopii zapasowych, zabezpieczeń i źródła danych
   ##### 1. Wybierz na jakiej zasadzie będą przechowywane kopie zapasowe bazy danych. W tym przypadku wybrany został tryb GRS, który zapewnia kopie zapasowe (tworzone asynchronicznie) w innym regonie niż oryginalny region serwera. Przeczytaj więcej: https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy
   ![image](https://github.com/user-attachments/assets/aba8a64f-0134-43e3-a584-0748fce84b73)

   ##### 2. Skonfiguruj zabezpieczenia bazy danych
   ![image](https://github.com/user-attachments/assets/a3ea05fd-c319-43fd-9eb4-ea7d6de221de)



   ##### 3. Skonfiguruj źródło danych, w tym przypadku została wybrana przykładowa baza danych.
   ![image](https://github.com/user-attachments/assets/138f1551-b52b-4ed6-a40c-5041392f0de0)


   Kliknij "Review + Create", po sprawdzeniu konfiguracji serwera, kliknij "Create"

   ### 2. Połączenie z bazą danych przy pomocy aplikacji do zarządzania bazami danych

   #### a. Połączenie do serwera za pomocą SSMS
   ##### 1. Przejdź do utworzonego zasobu, na głównym pulpicie skopiuj nazwę serwera
   ![image](https://github.com/user-attachments/assets/86c17edc-fbdc-4b9b-a6c4-2cc5cb803443)

   ##### 2. Następnie przejdź do SSMS, wpisz nazwę serwera oraz wybierz sposób autoryzacji ustawiony w trakcie konfiguracji.
   ![image](https://github.com/user-attachments/assets/9c893845-2b3d-412c-a6a0-b0e83598a95b)

   #### b. Połączenie do serwera za pomocą Azure Data Studio
   Z głównego ekranu Azure Data Studio wybierz "Create connection" i wpisz dane tak jak w przypadku SSMS
   ![image](https://github.com/user-attachments/assets/89eddab0-3f5b-4c7b-bce6-fee67dc74a16)

   ### 3. Połączenie z bazą danych za pomocą języka Python oraz SQLAlchemy do ORM
   #### a. Skonfigurowanie parametrów połączenia i zimportowanie odpowiednich modułów z SQLAlchemy 
   ```Python
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base


# Parametry połączenia
driver = 'ODBC Driver 18 for SQL Server'
server = 'jkserver1.database.windows.net'
port = '1433'
database = 'MyDb'
username = 'bleidd'
password = 'mypassword'

```

   #### b. Utworzenie bazowego modelu ORM oraz definicja tabeli ProductCategory
   ```Python
# Utwórz bazowy model ORM
Base = declarative_base()

# Definicja tabeli ProductCategory jako modelu ORM
class ProductCategory(Base):
    __tablename__ = 'ProductCategory'
    __table_args__ = {'schema': 'SalesLT'}
    ProductCategoryID = Column(Integer, primary_key=True)
    ParentProductCategoryID = Column(Integer)
    Name = Column(String)
    rowguid = Column(String)
    ModifiedDate = Column(Date)
```

   #### c. Konfiguracja połączenia i stworzenie sesji
   ```Python
# Skonfiguruj połączenie
connection_string = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}" \
                    f"?driver={driver}&Encrypt=yes&TrustServerCertificate=no&Connection Timeout=30"
engine = create_engine(connection_string)

# Tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()
```


   #### d. Wywołanie query pobierającej dane z tabeli ProductCategory oraz wypisanie ich do konsoli
```Python
ProductCategories = session.query(ProductCategory).all()
print("Lista kategorii produktu:")
for ProductCategory in ProductCategories:
    print(f"ProductCategoryID: {ProductCategory.ProductCategoryID},"
          f" ParentProductCategoryID: {ProductCategory.ParentProductCategoryID},"
          f" Name: {ProductCategory.Name},"
          f" rowguid: {ProductCategory.rowguid}"
          f" ModifiedDate: {ProductCategory.ModifiedDate},")
```

   Wynik działania kodu:
   ![image](https://github.com/user-attachments/assets/0441fde9-14bf-40c0-bf95-8f461d304c4a)

   

### 3. Konfiguracja maszyny witualnej
Wejdź z pulpitu Azure w "Virtual Machines", następnie kliknij "Create"
Uzupełnij nazwę wirtualnej maszyny, wybierz obraz systemu, architekture - w tym przypadku jako obraz systemu został wybrany [gotowy obraz z SQL Server z Azure Marketplace](https://azuremarketplace.microsoft.com/en-GB/marketplace/apps/microsoftsqlserver.sql2022-ubuntupro2004)
![image](https://github.com/user-attachments/assets/ec9bf7c6-7c5f-466d-a445-1873120658f0)




Ustaw rozmar, konto administratora i otwarte porty
![image](https://github.com/user-attachments/assets/ecca78e0-a5c9-49ff-837e-1a61b462dcd1)

W zakładce "Management" aktywuj Microsoft Defender
![image](https://github.com/user-attachments/assets/b34a5c5e-5492-4539-a9bc-c448fd6f7ab8)

### 4. Połączenie z maszyną wirtualną przez SSH w Azure CLI
![image](https://github.com/user-attachments/assets/a8e4a05f-6841-42ed-a1fd-a18da0064bec)

#### Konfiguracja SQL Server
![image](https://github.com/user-attachments/assets/f7881ded-4943-4f15-8109-2e6453990574)

Następnie zainstaluj mssql-tools za pomocą komendy:
```sudo apt-get install mssql-tools18```
i dodaj do PATH
``echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bash_profile
source ~/.bash_profile``

Następnie połącz się z bazą danych za pomocą komendy
```sqlcmd -S your_server.database.windows.net -d your_database -U your_username -P your_password -N```
tak jak na poniższym zrzucie ekranu
![image](https://github.com/user-attachments/assets/9f758c96-9f82-4913-a0b3-14b420e8710f)


### 4. Azure Table Storage
#### a. Utwórz Storage Account
przejdź do zakładki "Storage Accounts" kliknij "Create"m
następnie uzupełnij nazwę konta, region i wybierz główną usługę
![image](https://github.com/user-attachments/assets/7a684c34-1110-4738-ad6d-75d448690be4)
Kliknij Review + Create


#### b. Utwórz nową tabele i dodaj dane
Przejdź do Storage Browser -> Tables -> Add Table,
Następnie przejdź do nowo utworzonej tabeli i kliknik "Add Entity"
#### c. Używanie Azure Storage SDK w Python
Zainstaluj Azure Data Tables SDK używając pip:
``` pip install azure-data-tables```

Następnie znajdź Connection String wchodząc w utworzone konto Storage -> Security + Networking -> Access Keys
![image](https://github.com/user-attachments/assets/2559941d-6690-43a7-919d-10ab9ad4f713)


Utworzenie połączenia do odpowiedniej tabeli:
```Python
from azure.data.tables import TableServiceClient, TableClient, UpdateMode
from azure.data.tables import TableEntity
connection_string = "yourconnectionstring"
table_name = "newtable"

service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = service_client.get_table_client(table_name)
```
Obsługa operacji CRUD:
Create: 
```Python
def create_entity():
    entity = TableEntity(
        PartitionKey="partition1",
        RowKey="row1",
        name="Sample Entity",
    )
    table_client.create_entity(entity=entity)
    print(f"Entity created: {entity}")
```

Read:
```Python
def read_entity(partition_key, row_key):
    try:
        entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
        print(f"Entity retrieved: {entity}")
    except Exception as e:
        print(f"Error retrieving entity: {e}")
```
Update:
```Python
def update_entity(partition_key, row_key):
    entity = {
        "PartitionKey": partition_key,
        "RowKey": row_key,
        "name": "Updated Entity",
    }
    table_client.update_entity(entity=entity, mode=UpdateMode.MERGE)
    print(f"Entity updated: {entity}")
```
Delete:
```Python
def delete_entity(partition_key, row_key):
    table_client.delete_entity(partition_key=partition_key, row_key=row_key)
    print(f"Entity with PartitionKey='{partition_key}' and RowKey='{row_key}' deleted.")
```
Wypisanie wszystkich danych z Tabeli:
```Python
def read_all_entities():
    entities = table_client.list_entities()
    print("All Entities in the Table:")
    for entity in entities:
        print(entity)
```

Przykładowy program korzystający z wyżej zaimplementowanych operacji:
```Python
    read_all_entities()

    create_entity()

    read_entity("partition1", "row1")

    update_entity("partition1", "row1")

    read_entity("partition1", "row1")

    read_all_entities()

    delete_entity("partition1", "row1")
```
Wynik działania kodu:

![image](https://github.com/user-attachments/assets/ba694c62-7ee0-4bd6-a0f4-922f82775975)


### 5. Dodanie reguł firewalla do bazy danych Azure SQL
Wejdź w ustawienia Security -> Networking wybranej bazy danych

![image](https://github.com/user-attachments/assets/d737ad2a-0eb0-423b-9cd0-b4877188b565)

### 6. Azure Cosmos DB
Wejdź w All services -> Azure Cosmos DB -> kliknij "Create" i uzupełnij nazwę konta, wybierz serwer.

![image](https://github.com/user-attachments/assets/7a7f9dc6-f42b-4e12-9ce3-db83f3320a9f)

Przejdź do Data Explorer -> New Container w celu utworzenia nowego kontenera

![image](https://github.com/user-attachments/assets/2b76f0b2-8d2e-426b-b45c-fa9a47a0a9d2)

Przejdź do stworzonej bazy i kontenera -> Items -> New Item:

![image](https://github.com/user-attachments/assets/cc2a3a73-2665-4ed2-b06a-1f87914769ff)

Przykładowe zapytanie filtrujące po warunku c.id = "2"

![image](https://github.com/user-attachments/assets/3ab5e46c-e847-4475-9c44-30db2f99d10a)


Kontrolowanie skalowania poziomego oraz liczby jednostek przetwarzania żądania RU/s jest dostępne po wejściu w Data Explorer -> kliknięcie zębatki w prawym górnym rogu:

![image](https://github.com/user-attachments/assets/80da6c05-ef35-4704-a130-54d52eb79b83)

![image](https://github.com/user-attachments/assets/7b0016ee-e41b-4c95-8961-65a0801b63fe)


### 7. Azure Cosmos DB SDK w Pythonie

Zainstaluj bibliotekę SDK dla Cosmos DB:

```pip install azure-cosmos```

---
Implementacja prostej aplikacji CRUD w Pythonie:

Konfiguracja parametrów połączenia i pobranie klienta kontenera:
```Python
from azure.cosmos import CosmosClient, exceptions

endpoint = "https://ratatoullecosmosacc.documents.azure.com:443/"
key = "OeclSlQ3Bthg99Ig7EqiFAbiZgoh3EYqhetqsvwLvNBr65auTtrNbS2gTCOS8ib0oiXPuASAhytFACDbvORRJA=="
database_name = "mydb1"
container_name = "cont"

client = CosmosClient(endpoint, key)
database = client.create_database_if_not_exists(id=database_name)
container = database.get_container_client(container_name)
```

Obsługa operacji CRUD:
Create:
```Python
def create_item(item):
    try:
        container.create_item(body=item)
        print("Dodano element:", item)
    except exceptions.CosmosHttpResponseError as e:
        print("Błąd podczas tworzenia elementu:", e)
```

Read:

```Python
    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        print("Odczytano element:", item)
        return item
    except exceptions.CosmosResourceNotFoundError:
        print(f"Element o ID {item_id} nie istnieje.")
    except exceptions.CosmosHttpResponseError as e:
        print("Błąd podczas odczytu elementu:", e)
```

Update:

```Python
def update_item(item_id, partition_key, updated_fields):
    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        for key, value in updated_fields.items():
            item[key] = value
        container.upsert_item(body=item)
        print("Zaktualizowano element:", item)
    except exceptions.CosmosHttpResponseError as e:
        print("Błąd podczas aktualizacji elementu:", e)
```

Delete:

```
def delete_item(item_id, partition_key):
    try:
        container.delete_item(item=item_id, partition_key=partition_key)
        print(f"Usunięto element o ID: {item_id}")
    except exceptions.CosmosResourceNotFoundError:
        print(f"Element o ID {item_id} nie istnieje.")
    except exceptions.CosmosHttpResponseError as e:
        print("Błąd podczas usuwania elementu:", e)
```


Przykładowy program wykorzystujący powyższe operacje:

```
  id = "10"
    # Dodaj nowy dokument
    new_item = {
        "id": id,
        "name": "Example Item",
    }
    create_item(new_item)

    # Odczytaj dokument
    read_item(id, id)

    # Zaktualizuj dokument
    update_fields = {"name": "Updated Name"}
    update_item(id, id, update_fields)

    # Ponownie odczytaj zaktualizowany dokument
    read_item(id, id)

    # Usuń dokument
    delete_item(id, id)
```
Wynik działania programu:

![image](https://github.com/user-attachments/assets/ea0cd8fc-ecf5-4b23-b4ee-0c4efd9fe7d2)










