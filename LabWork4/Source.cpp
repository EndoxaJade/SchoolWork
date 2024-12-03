#include <iostream>
#include <vector>
#include <crtdbg.h>
#define _CRTDBG_MAP_ALLOC

using namespace std;

class Person {
private: 
	string name;
	int age;
public:
	Person(string name = "No-name", int age = 0) : name{name}, age{age} {} //Конструктор
	void GetDataP(string uname, int uage) {
		name = uname;
		age = uage;
	}
	void PrintDataP() {
		cout << "Person's name: " << name << "\nPerson's age: " << age << endl;
	}
};

template<typename T, typename T1, typename T2>
class Occupant : public Person {
private:
	string occupation;
	T id;
	T1 salary;
	T2 schoolnum;
public: //Конструктор v
	Occupant(string occupation = "None", T id = 0, T1 salary = 0, T2 schoolnum = 0) : occupation{ occupation }, id{ id }, salary{ salary }, schoolnum{ schoolnum } {}
	void PrintData() {
		cout << "Person's occupation: " << occupation << "\nPerson's id: " << id << "\nPerson's salary: " << salary << "\nPerson's school number: " << schoolnum << endl;
	}
};
template<typename T>
class Counter {
private:
	vector<T> address{};
public:
	void GetAddress(T ar) {
		address.push_back(ar);
	}
	void PrintAddress() {
		for (int i = 0; i < address.size(); i++) {
			cout << address[i] << " ";
		}
		cout << "\n";
	}
};

int main(){
	Person mom;
	mom.GetDataP("Dillia", 39);
	mom.PrintDataP();
	Person dad;
	cout << "\n";
	Occupant<string, string, string> me("Pre-schooler", "wats an ID?", "milion dolar monny", "2936192");;
	me.PrintData();
	cout << "\n";
	Occupant<string, string, int> mary("Schoolgirl", "none", "none", 967);
	mary.PrintData();
	cout << "\n";
	Occupant<string, float, int> student("Student", "IDB-23-08b", 4392.50, 924);
	student.GetDataP("Evelyn", 19);
	student.PrintDataP();
	student.PrintData();
	cout << "\n";
	Occupant<int, int, string> bob("Employee", 1003, 5700, "Viridian school of Lawrence J.");
	bob.PrintData();
	cout << "\n";
	Person* pt = &mom;
	Person* pt2 = &dad;
	Occupant<string, float, int>* pt3 = &student;
	Counter<Person*> box;
	box.GetAddress(pt);
	box.GetAddress(pt2);
	box.PrintAddress();
	cout << "\n";
	Counter< Occupant<string, float, int>*> korobka;
	korobka.GetAddress(pt3);
	korobka.PrintAddress();
	_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_DEBUG);
	_CrtDumpMemoryLeaks();
	return 0;
}
