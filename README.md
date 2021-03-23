# *Dhaka Stock Exchange(DSE)* Momentum Trading Strategy
Recommends a list of stocks to buy based on a momentum trading strategy

## Usage 
The function *momentum_strategy* has the following properties: 

Parameters:
* start (str): Start date
* end (str): End date
* formation (str): portfolio formation date
* rolling_months (int): no of months rolling period 

Returns:
* momentum_profit (float64): mean of winner stock returns for latest month
* winners(list): list of winner stocks


Stuff to do
- [ ] Implement more strategies
- [ ] Documentation
- [ ] Make into a Python Package
