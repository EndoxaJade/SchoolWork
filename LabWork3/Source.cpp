#include <iostream>
#include <vector>
using namespace std;
class Assembly {
private:
int serialNum = 1989;
friend void showA();
protected:
Assembly() {} //Конструктор
public:
void GetData() {
cout << "Assembly serial number: " << serialNum << endl;
}
void say() {
cout << "Last checked: December 12, 1997\n";
}
};
 
class Part: public Assembly {
private:
int weight = 190, num = 12;
friend void showA();
protected:
Part() {} //Конструктор
public:
void GetData() {
cout << "Part's weight: " << weight << "\nPart's number: " << num << endl;
}
};

class Base {
public:
	virtual void write() {
		cout << "Greetings, Earth! I'm class Base =)";
	}
	virtual ~Base() = default; //Деструктор
};

class Derived : public Base {
public:
	void write() override {
		cout << "Hello, world! I'm class Derived >O<";
	}
};
 
void showA() {
Assembly a1;
Part p1;
Part p2;
vector<Assembly> storage;
storage.push_back(p1);
storage.push_back(p2);
for (int i = 0; i < 2; i++) {
storage[i].GetData();
}
vector<Part> storage2;
storage2.push_back(p2);
storage2[0].GetData();
storage2[0].say();
}
int main() {
showA();
vector<unique_ptr<Base>> box; //Хранилище объектов классов
srand(time(0)); //Меняем сид рандомайзера чисел
int ranNum = 0;
for (int i = 0; i < 3; i++) { //Создание трёх экземпляров классов
	ranNum = rand();
	if (ranNum % 2 == 0) {
		box.push_back(make_unique<Base>());
	}
	else {
		box.push_back(make_unique<Derived>());
	}
}
for (const auto& o : box) { //Освобождение памяти происходит автоматически, поскольку не было использовано оператора new
	o->write();
	cout << endl;
}
return 0;
}