#include <iostream>
#include <string>
using namespace std;
class Publication { // Базовый класс издательства
public:
	string name;
	float cost;
};
class Sales { // Базовый класс продаж
public:
	float M[3];
};
class Book : public Publication, public Sales { // Наследник с количеством страниц
private:
	int pages;
public:
	void GetData(string uname, float ucost, int upages) {
		name = uname;
		cost = ucost;
		pages = upages;
		cout << "\nEnter sales of the book for the past three months\n";
		cin >> M[0] >> M[1] >> M[2];
	}
	void PutData() {
		cout << "Book name: " << name << "\nBook cost: " << cost <<
			"\nNumber of pages: " << pages << "\nSales: ";
		for (int i = 0; i < 3; i++) {
			cout << M[i] << " ";
		}
		cout << "\n";
	}
};
class Type : public Publication, public Sales { // Наследник с длительностью аудиозаписи
private:
	int timeMin;
public:
	void GetData(string uname, float ucost, int utime) {
		name = uname;
		cost = ucost;
		timeMin = utime;
		cout << "\nEnter sales of the book for the past three months\n";
		cin >> M[0] >> M[1] >> M[2];
	}
	void PutData() {
		cout << "Book name: " << name << "\nBook cost: " << cost <<
			"\nAudio length: " << timeMin << " minutes" << "\nSales: ";
		for (int i = 0; i < 3; i++) {
			cout << M[i] << " ";
		}
		cout << "\n";
	}
};
int main() {
	string N; float C; int P; int T;
	Book book1;
	Type book2;
	cout << "Enter first book name, cost and number of pages\n";
	cin >> N >> C >> P;
	book1.GetData(N, C, P);
	book1.PutData();
	cout << "Enter second book name, cost and audio length\n";
	cin >> N >> C >> T;
	book2.GetData(N, C, T);
	book2.PutData();
	return 0;
}
