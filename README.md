# GeothermalStockModelling
Definition of an Optimized Geothermal Utilization Strategy using Stock Reservoir Modelling as a Foundation

This model was created by Arkaitz Manterola Donoso for the Master Thesis named '*Optimization of Sustainable Production Strategy for Geothermal Power Plants using Stock Reservoir Modelling*'. 

There are two main models to the code. A stock model and a production strategy model.

The first model will solve the main parameters required to describe a geothermal reservoir stock model. To do so, external data of the production wells will be requried. This model will be required as said main parameters will be then part of the initial inputs of the strategy model. 

The second model will create a production strategy focused on increasing the general revenue of the power plant while reducing the environmental impacts of the extraction (carbon emissions, excessive brine extraction and reservoir pressure drawdown)

**About the files in this repository:**

  **Provided code:**
    *main.py* is the main code, which will solve both models (stock and production strategy). 
    *residaulmse* contains all equations needed to define the stock model and to calculate the sum of squares of the residuals for the stock model parametrization
    *production_eq* contains all equations needed to define and solve the production strategy model

  **Provided databases:**
    *BJ-11* and *BJ-12* contain data from wells BJ-11 and BJ-12 from the Bjarnarflag Power Station provided by Landsvirkjun. The dataset contains data throught different measurements over time. There is data on *Pressure* (bars), *Flow* (kg/s), *Enthalpy* (kJ/kg), *Well Status* (open, closed or bleed) and *Data quality* (Good, Fair, Suspect or Estimated). Additionally, time (*t*) has been calculated in years since the beginning of 2019, to be able to calculate time differentials (*Dt*) for each timestep. Extraction values from known data have been calculated from enthalpy and flow values in column *Extraction_d*. Additional columns *Stock*, *Recharge* and   *Extraction* will be calculated by the model together by *Diff*, which measures the difference between extraction calculated from data and from the model (Eq. 8 in   the Master Thesis). 
    *Production_5y* containts the final strategy model results using all the specified parameters and values in the case study. 
    *Production_5y_noCO2* constaints the final strategy model results if the carbon tax is not considered. 
