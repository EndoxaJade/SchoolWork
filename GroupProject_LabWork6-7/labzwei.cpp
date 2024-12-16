#include <iostream> 
#include <string> 
#include <fstream> 
#include <vector>
#include <cmath> 
using namespace std;

const char alphabet[64] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '=' }; // Алфавит base64 

// Переменная для выбора операции 
int decision = 0; // Переменная, определяющая то, что мы будем делать с файлом 
// Переменные для кодирования 
char c1; char c2; char c3; // Переменные символов 
int asciic1; int asciic2; int asciic3; int asciic3dub; // Символы в ASCII для кодирования 
int res; // Результат обработки 1-го символа 
int res11; int res12; int res1; // Результаты обработки 1 и 2-го символа 
int res22; int res23; int res2; // Результаты обработки 2 и 3-го символов 
int res3; // Результат обработки 3-го символа 


int main() {
	cout << "Hello there! To encode a file type 0. To decode a file type 1.\n";
	cin >> decision;
	if (decision == 0) {
		ifstream fin("Code.txt");
		int charCount = 0; // Подсчет количества символов в файле 
		char c;
		while (!fin.eof()) {
			c = fin.get();
			cout << c; // Выводим читаемый файл 
			charCount++;
		}
		fin.close();
		double count = charCount - 1;
		cout << "\nNumber of characters in a string: " << count << endl; // Выводим количество символов в файле 
		cout << "Your string in base64 will be: ";
		ifstream fin1("Code.txt");
		for (int i = 0; i < ceil(count / 3); i++) {
			// Обработка трех символов 
			c1 = fin1.get(); // Читаем первый символ 
			c2 = fin1.get(); // Читаем второй символ 
			c3 = fin1.get(); // Читаем третий символ 
			//cout << "\n" << c1 << " " << c2 << " " << c3 << endl; 
			asciic1 = static_cast<int>(c1); // Преобразуем в целое для манипуляций битами 
			asciic2 = static_cast<int>(c2);
			asciic3 = static_cast<int>(c3);
			asciic3dub = asciic3; // Сделаем дубликат третьего символа, чтобы при необходимости вывести = в base64 
			//cout << asciic1 << " " << asciic2 << " " << asciic3 << endl; 
			if ((count == 4 || count == 5) && asciic2 == -1) { asciic2 = 0; }
			if (count == 5 && asciic3 == -1) { asciic3 = 0; }
			//cout << asciic1 << endl; // Проверка символов в ASCII 
			//cout << asciic2 << endl; 
			//cout << asciic3 << endl; 
			// Шаг 1 
			res = asciic1 >> 2; // Сдвигаем первый символ вправо на 2 
			// Шаг 2 
			res11 = asciic1 << 4; // Сдвигаем первый символ влево на 4 
			res12 = asciic2 >> 4; // Сдвигаем второй символ вправо на 4 
			res1 = res11 | res12; // Склеиваем результаты 
			res1 = res1 & 63; // Оставляем только 6 младших бит 
			// Шаг 3 
			res22 = asciic2 << 2; // Сдвигаем второй символ влево на 2 
			res23 = asciic3 >> 6; // Сдвигаем третий символ вправо на 6 
			res2 = res22 | res23;
			res2 = res2 & 63;
			// Шаг 4 
			res3 = asciic3dub & 63;
			// Выводим символы в base64 
			cout << alphabet[res];
			cout << alphabet[res1];
			cout << alphabet[res2];
			cout << alphabet[res3];
		}
		fin1.close();
	}
	else if (decision == 1) {
		cout << "Jenya's code here\n";
		ifstream f("Code.txt");
		string b;
		for (int i = 0; i < 4; i = i + 1) {
			char c;
			f.get(c);
			b = b + c;
		}
		f.close();
		vector<int> in(4);
		for (int i = 0; i < 4; i = i + 1) {
			for (int j = 0; j < 64; j = j + 1) {
				if (b[i] == alphabet[j]) {
					in[i] = j;
					break;
				}
			}
		}
		int by1 = (in[0] << 2) | (in[1] >> 4);
		int by2 = (in[1] << 4) | (in[2] >> 2);
		int by3 = (in[2] << 6) | (in[3]);
		string res;
		res = res + static_cast<char>(by1);
		res = res + static_cast<char>(by2);
		res = res + static_cast<char>(by3);
		cout << "Decoded: " << res << endl;
	}
	else {
		cout << "Oops! It seems you typed the wrong number! Close the console and try again ;-)";
	}
	return 0;
} 