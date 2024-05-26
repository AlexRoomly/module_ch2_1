import queue
import time
import threading


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Customer(threading.Thread):

    def __init__(self, name, number_table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.number_table = number_table


    def run(self):

        cafe.serve_customer(customer=self.name)
        print(f'Посетитель номер {self.name} покушал и ушёл', flush=True)


class Cafe:
    def __init__(self, tables):
        self.tables = tables
        # очередь посетителей (создаётся внутри init)
        self.ocher = queue.Queue()
        self.customer = 0
        self.customers_size = 20

    def customer_arrival(self):

        customers = []
        for i in range(self.customers_size):
            customer = Customer(name=str(i + 1), number_table=0)
            print(f'Посетитель номер {str(i + 1)} прибыл.', flush=True)
            customers.append(customer)
            time.sleep(1)
            customer.start()
        for customer in customers:
            customer.join()

        # моделирует приход посетителя(каждую секунду)

    def serve_customer(self, customer):
        if int(customer) > len(self.tables):
            print(f'Посетитель номер {customer}  ожидает свободный стол.', flush=True)
        self.ocher.put(customer)

        what_table = 0

        def cafe_table(x):
            free_table = x
            for table in self.tables:
                if table.is_busy == False:
                    free_table = table.number
                    table.is_busy = True
                    break
            return (free_table)

        this_table = cafe_table(what_table)

        def table_busy():
            customer = self.ocher.get()
            self.customer = customer
            print(f'Посетитель номер {self.customer} сел за стол {this_table}.', flush=True)
            time.sleep(5)
            self.tables[this_table - 1].is_busy = False
            return

        if this_table > 0:
            return table_busy()

        else:
            while not this_table:
                time.sleep(1)
                this_table = cafe_table(0)
            table_busy()


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
