#include <iostream>
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#include <string>
using namespace std;
class Library {
private:
	string author, name, type;
public:
	Library(string uauthor = "Unauthored", string uname = "Unnamed", string utype = "Fiction") { // Конструктор
		setBook(uauthor, uname, utype);
	}
	void setBook(string uauthor, string uname, string utype) {
		author = uauthor;
		name = uname;
		type = utype;
	}
	void getBook() {
		cout << "Author: " << author << "\nName: " << name << "\nType: " << type;
	}
};

int main() {
	int n; // Размер массива
	cout << "Number 1, var A\n";
	cout << "Enter size of the list\n";
	cin >> n;
	int* M = new int[n]; // Объявление массива
	cout << "Fill the list\n";
	for (int i = 0; i < n; i++) {
		cin >> M[i];
	}
	for (int i = 0; i < n; i++) { // Вывод массива
		cout << M[i] << " ";
	}
	cout << "\nAdress of the beginning: " << &M[0];
	for (int i = 1; i < n; i++) {
		cout << "\n" << &M[i];
	}
	cout << "\nElements of the list are located 4 blocks away from each other";
	delete[] M;
	string A, N, T; // Добавление пользовательских книг
	Library book1("Engels", "Tech and Such", "Technical");
	book1.getBook();
	cout << "\nAdd a book. Who is the author? What is the name? What is the type?\n";
	cin >> A;
	cin >> N;
	cin >> T;
	Library book2;
	book2.setBook(A, N, T);
	book2.getBook();
	cout << "\n";
	Library book3;
	book3.getBook();
	_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_DEBUG);
	_CrtDumpMemoryLeaks();
	return 0;
}
