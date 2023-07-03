# GeothermalStockModelling
Definition of an Optimized Geothermal Utilization Strategy using Stock Reservoir Modelling as a Foundation

This model was created by Arkaitz Manterola Donoso for the Master Thesis named '*Optimization of Sustainable Production Strategy for Geothermal Power Plants using Stock Reservoir Modelling*'. The final document, with additional details, can be found in Skemman (http://hdl.handle.net/1946/42384). 

There are two main models to the code. A stock model and a production strategy model.

The first model will solve the main parameters required to describe a geothermal reservoir stock model. To do so, external data on the production wells will be required. This model will be required as said main parameters will be then part of the initial inputs of the strategy model. 

The second model will create a production strategy focused on increasing the general revenue of the power plant while reducing the environmental impacts of the extraction (carbon emissions, excessive brine extraction, and reservoir pressure drawdown)

**About the files in this repository:**

*Provided code:* <br />
-**main.py** is the main code, which will solve both models (stock and production strategy). <br />
-**residaulmse.py** contains all equations needed to define the stock model and to calculate the sum of squares of the residuals for the stock model parametrization. <br /> 
-**production.py** contains all equations needed to define and solve the production strategy model. <br />

*Provided databases:* <br />
-**BJ-11.xlsx** and **BJ-12.xlsx** contain data from wells BJ-11 and BJ-12 from the Bjarnarflag Power Station provided by Landsvirkjun. The dataset contains data through different measurements over time. There is data on *Pressure* (bars), *Flow* (kg/s), *Enthalpy* (kJ/kg), *Well Status* (open, closed or bleed), and *Data quality* (Good, Fair, Suspect or Estimated). Additionally, time (*t*) has been calculated in years since the beginning of 2019, to be able to calculate time differentials (*Dt*) for each timestep. Extraction values from known data have been calculated from enthalpy and flow values in column *Extraction_d*. Additional columns *Stock* in MWyr, *Recharge* in MW and *Extraction* in MW will be calculated by the model together by *Diff*, which measures the difference between extraction calculated from data and from the model (Eq. in 9 the Master Thesis). <br />
-**Production_5y.xlsx** contains the final strategy model results using all the specified parameters and values in the case study. The shown parameters and units are: *Year* (Time in years), *P11* (Pressure of BJ-11 in bars),	*S11* (Stock of BJ-11 in MWyr),	*E11* (Extraction rate of BJ-11 in MW), *R11* (Recharge rate of BJ-11 in MW),	*H11*	(Enthalpy of BJ-11 in kJ/kg), *TF11*	(Total flow of BJ-11 in kg/s), *SF11*	(Steam flow of BJ-11 in kg/s), *LF11* (Liquid flow of BJ-11 in kg/s), P12 (Pressure of BJ-12 in bars), *S12* (Stock of BJ-12 in MWyr),	*E12* (Extraction rate of BJ-12 in MW), *R12* (Recharge rate of BJ-12 in MW),	*H12*	(Enthalpy of BJ-12 in kJ/kg), *TF12*	(Total flow of BJ-12 in kg/s), *SF12*	(Steam flow of BJ-12 in kg/s), *LF12* (Liquid flow of BJ-12 in kg/s), *Obj*	(objective function value in $/h), *Total Steam* (Steam from both wells in kg/s), *Total Water*	(Brine from both wells in kg/s), *CO211* (CO2 Emissions from BJ-11 in mg/s), *CO212* (CO2 Emissions from BJ-12 in mg/s),	*Total CO2* (CO2 Emissions from both wells in mg/s)<br />
-**Production_5y_noCO2.xlsx** contains the final strategy model results if the carbon tax is not considered. The studied parameters are the same as for *production_5y.xlsx* <br />

*Provided figures:* <br />
-**Productivity curves (August 2021).png** shows the productivity curves of wells BJ-11 abd BJ-12 in August 2021. <br />
-**Decline curve BJ-11.png** and **Decline curve BJ-12.png** show the change in the productivity of the wells considering the existing data between 2018 and 2022. <br />
-**Production history BJ-11.png** and **Production history BJ-12.png** show how each of the wells has been utilized throughout the studied time frame. <br />

The code has been specifically built to solve the case study for Bjarnarflag Power Station. However, with small changes in different parts of the code, the code could be adapted to studies in other locations and with different characteristics. These changes can be pertaining to different estimations and information for this specific study:
- Having different initial databases instead of the ones provided for both wells (if this is the case, linear equations for enthalpy and steam ratio, as well as carbon dioxide parameters and well boundaries would have to be overanalyzed and changed in *production.py* and in *main.py*). 
- The objective coefficients (changes in prices) can be easily implemented in *production.py* file. 
- Different extraction periods and timesteps can be applied to get more general or more specific data in *main.py* (the more data points wanted the more the code can take to solve)
- Additional constraints can be added if needed (inequality constraints should be similar to cons1 and equality constraints to stock_balance in *production.py*) or the objective function changed in the case of working with a different system with different needs. <br />
