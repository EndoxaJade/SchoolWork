#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
using namespace std;

const char alphabet[64] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '='}; //Алфавит base64

//Определяем используемые переменные
int decision = 0; //Переменная, управляющвя тем, что мы будем делать с файлом
//Переменные для кодирования
char c1; char c2; char c3; //Переменные символов
int asciic1; int asciic2; int asciic3; int asciic3dub; //Символы в ASCII кодировке
int res; //Результат обработки 1 символа
int res11; int res12; int res1; //Результаты обработки 1 и 2 символа
int res22; int res23; int res2; //Результаты обработки 2 и 3 символов
int res3; //Результат обработки 3 
//Переменные для декодирования


int main() {
	cout << "Hello there! To encode a file type 0. To decode a file type 1.\n";
	cin >> decision;
	if (decision == 0) {
		ifstream fin("Code.txt");
		int charCount = 0; //Считаем количество символов в файле
		char c;
		while (!fin.eof()) {
			c = fin.get();
			cout << c; //Выводим содержимое файла
			charCount++;
		}
		fin.close();
		double count = charCount - 1;
		cout << "\nNumber of characters in a string: " << count << endl; //Выводим количество символов в файле
		cout << "Your string in base64 will be: ";
		ifstream fin1("Code.txt");
		for (int i = 0; i < ceil(count / 3); i++) {
			//Обработка тройки символов
			c1 = fin1.get(); //Считанный первый символ
			c2 = fin1.get(); //Считанный второй символ
			c3 = fin1.get(); //Считанный третий символ
			//cout << "\n" << c1 << " " << c2 << " " << c3 << endl;
			asciic1 = static_cast<int>(c1); //Переводим в число для совершения побитовых операций
			asciic2 = static_cast<int>(c2);
			asciic3 = static_cast<int>(c3);
			asciic3dub = asciic3; //Определим дубликат третьего байта из набора, чтобы правильно выводить = в base64
			//cout << asciic1 << " " << asciic2 << " " << asciic3 << endl;
			if ((count == 4 || count == 5) && asciic2 == -1) { asciic2 = 0; }
			if (count == 5 && asciic3 == -1) { asciic3 = 0; }
			//cout << asciic1 << endl; //Проверка символов в ASCII
			//cout << asciic2 << endl;
			//cout << asciic3 << endl;
			//Шаг 1 алгоритма STEP 1
			res = asciic1 >> 2; //Делаем побитовый сдвиг вправо на 2
			//Шаг 2 алгоритма STEP 2
			res11 = asciic1 << 4; //Делаем побитовый сдвиг влево на 4
			res12 = asciic2 >> 4; //Делаем побитовый сдвиг вправо на 4
			res1 = res11 | res12; //Делаем побитовое или
			res1 = res1 & 63; //Делаем побитовое и для избавления от 2 старших разрядов
			//Шаг 3 алгоритма STEP 3
			res22 = asciic2 << 2; //Делаем побитовый сдвиг влево на 2
			res23 = asciic3 >> 6; //Делаем побитовый сдвиг вправо на 6
			res2 = res22 | res23;
			res2 = res2 & 63;
			//Шаг 4 алгоритма STEP 4
			res3 = asciic3dub & 63;
			//Выводим символы из base64 в качестве результата
			cout << alphabet[res];
			cout << alphabet[res1];
			cout << alphabet[res2];
			cout << alphabet[res3];
		}
		fin1.close();
	}
	else if(decision == 1) {
		cout << "Jenya's code here\n";
	}
	else {
		cout << "Oops! It seems you typed the wrong number! Close the console and try again ;-)";
	}
	return 0;
}