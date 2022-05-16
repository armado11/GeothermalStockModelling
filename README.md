# GeothermalStockModelling
Definition of an Optimized Geothermal Utilization Strategy using Stock Reservoir Modelling as a Foundation

This model was created by Arkaitz Manterola Donoso for the Master Thesis named '*Optimization of Sustainable Production Strategy for Geothermal Power Plants using Stock Reservoir Modelling*'. 

There are two main models to the code. A stock model and a production strategy model.

The first model will solve the main parameters required to describe a geothermal reservoir stock model. To do so, external data of the production wells will be requried. This model will be required as said main parameters will be then part of the initial inputs of the strategy model. 

The second model will create a production strategy focused on increasing the general revenue of the power plant while reducing the environmental impacts of the extraction (carbon emissions, excessive brine extraction and reservoir pressure drawdown)

**About the files in this repository:**

*Provided code:* <br />
-**main.py** is the main code, which will solve both models (stock and production strategy). <br />
-**residaulmse** contains all equations needed to define the stock model and to calculate the sum of squares of the residuals for the stock model parametrization. <br /> 
-**production** contains all equations needed to define and solve the production strategy model. <br />

*Provided databases:* <br />
-**BJ-11** and **BJ-12** contain data from wells BJ-11 and BJ-12 from the Bjarnarflag Power Station provided by Landsvirkjun. The dataset contains data throught different measurements over time. There is data on *Pressure* (bars), *Flow* (kg/s), *Enthalpy* (kJ/kg), *Well Status* (open, closed or bleed) and *Data quality* (Good, Fair, Suspect or Estimated). Additionally, time (*t*) has been calculated in years since the beginning of 2019, to be able to calculate time differentials (*Dt*) for each timestep. Extraction values from known data have been calculated from enthalpy and flow values in column *Extraction_d*. Additional columns *Stock* in MWyr, *Recharge* in MW and *Extraction* in MW will be calculated by the model together by *Diff*, which measures the difference between extraction calculated from data and from the model (Eq. in 9 the Master Thesis). <br />
-**Production_5y** containts the final strategy model results using all the specified parameters and values in the case study. <br />
-**Production_5y_noCO2** constaints the final strategy model results if the carbon tax is not considered. <br />

The code has been specifically built to solve the case study for Bjarnarflag Power Station. However, with small changes on different parts of the code, the code could be adapted to studies in other locations and with different characteristics. These changes can be pertaining to different estimations and information for this specific study:
- Having different initial databases instead of the ones provided for both wells (if this is the case, linear equations for enthaply and steam ratio, as well as carbon dioxide parameters and well boundaries would have to be overanalised and changed in *production.py* and in *main.py*). 
- The objective coefficients (changes in prices) can be easily implemented in *production.py* file. 
- Different extraction periods and timesteps can be applied to get more general or more specific data in *main.py* (the more datapoints wanted the more the code can take to solve)
- Additional constraints can be added if needed (inequality constraints should be similar to cons1 and equality constraints to stock_balance in *production.py*) or the objective function changed in the case of working with a different system with different needs. <br />
