#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <numeric>

void main() {
	setlocale(LC_ALL, "Russian");
	std::fstream input{"input.txt"};

	double gamma;
	double time_infail;
	double time_fail;

	std::vector<double> times;

	input >> gamma;
	input >> time_infail;
	input >> time_fail;

	double in;
	while (input >> in) {
		times.push_back(in);
	}

	std::sort(times.begin(), times.end());

	double average = std::accumulate(std::next(times.begin()), times.end(), times[0]) / times.size();
	double h = (times.back() - times.front()) / 10;

	std::vector<double> f_list{};
	f_list.push_back(0);
	std::vector<double> p_list{};
	p_list.push_back(1);

	uint32_t i = 0, index = 0, c1 = 0;
	for (uint32_t k = 1; k <= 11; ++k) {
		uint32_t c = 0;
		while (i < times.size() && times[i] <= k + h + times.front()) {
			c++;
			c1++;
			i++;
		}
		f_list.push_back(c / (h * times.size()));
		auto q = static_cast<double>(c1) / times.size();
		p_list.push_back(1 - q);
		if (p_list[k - 1] > gamma && gamma >= p_list[k])
			index = k;
	}
	auto d = (p_list[index - 1] - gamma) / (p_list[index - 1] - p_list[index]);
	auto t = f_list[index - 1] + h * d;

	double p = 1;
	uint32_t k = 1;

	while (k * h <= time_infail) {
		p -= f_list[k] * h;
		k++;
	}
	p -= f_list[k] * (time_infail - (k - 1) * h);

	double pf = 1;
	k = 1;

	while (k * h <= time_fail) {
		pf -= f_list[k] * h;
		k++;
	}
	pf -= f_list[k] * (time_fail - (k - 1) * h);
	auto lambd = f_list[k] / pf;

	std::cout << "Среднее время наработки наотказ: " << average 
		<< "\nВремя наработки наотказ при заданной вероятности: " << t 
		<< "\nВероятность безотказной рабьоты к заданному времени: " << p 
		<< "\nИнтесивность отказов за заданное время: "  << std::scientific << lambd << std::endl;
}