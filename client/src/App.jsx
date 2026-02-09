import React, { useState } from "react";
import Dropdown from "./components/Dropdown";
import NumericInput from "./components/NumericaInput";
import * as options from "./utils/options";
import axios from "axios";

const App = () => {
  const [formData, setFormData] = useState({
    gender: "",
    seniorCitizen: "",
    partner: "",
    dependents: "",
    tenure: 0,
    phoneService: "",
    multipleLines: "",
    internetService: "",
    onlineSecurity: "",
    onlineBackup: "",
    deviceProtection: "",
    techSupport: "",
    streamingTV: "",
    streamingMovies: "",
    contract: "",
    paperlessBilling: "",
    paymentMethod: "",
    monthlyCharges: 0,
    totalCharges: 0,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("http://13.204.154.162:8000/predict", {
        gender: formData.gender,
        SeniorCitizen: formData.seniorCitizen,
        Partner: formData.partner,
        Dependents: formData.dependents,
        tenure: Number(formData.tenure) || 0,
        PhoneService: formData.phoneService,
        MultipleLines: formData.multipleLines,
        InternetService: formData.internetService,
        OnlineSecurity: formData.onlineSecurity,
        OnlineBackup: formData.onlineBackup,
        DeviceProtection: formData.deviceProtection,
        TechSupport: formData.techSupport,
        StreamingTV: formData.streamingTV,
        StreamingMovies: formData.streamingMovies,
        Contract: formData.contract,
        PaperlessBilling: formData.paperlessBilling,
        PaymentMethod: formData.paymentMethod,
        MonthlyCharges: Number(formData.monthlyCharges) || 0,
        TotalCharges: Number(formData.totalCharges) || 0,
      });

      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Prediction failed. Please check all fields.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-6xl bg-white rounded-lg shadow-sm border border-gray-100 p-8">
        <h1 className="text-3xl font-semibold text-gray-800 mb-8 text-center">
          Customer Churn Prediction
        </h1>

        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Dropdown
              label="Gender"
              options={options.genderOptions}
              value={formData.gender}
              onChange={(e) => handleChange("gender", e.target.value)}
            />
            <Dropdown
              label="Senior Citizen"
              options={options.seniorCitizenOptions}
              value={formData.seniorCitizen}
              onChange={(e) => handleChange("seniorCitizen", e.target.value)}
            />
            <Dropdown
              label="Partner"
              options={options.partnerOptions}
              value={formData.partner}
              onChange={(e) => handleChange("partner", e.target.value)}
            />
            <Dropdown
              label="Dependents"
              options={options.dependentsOptions}
              value={formData.dependents}
              onChange={(e) => handleChange("dependents", e.target.value)}
            />
            <NumericInput
              label="Tenure (months)"
              value={formData.tenure}
              placeholder="0"
              onChange={(e) => handleChange("tenure", e.target.value)}
            />
            <Dropdown
              label="Phone Service"
              options={options.phoneServiceOptions}
              value={formData.phoneService}
              onChange={(e) => handleChange("phoneService", e.target.value)}
            />
            <Dropdown
              label="Multiple Lines"
              options={options.multipleLinesOptions}
              value={formData.multipleLines}
              onChange={(e) => handleChange("multipleLines", e.target.value)}
            />
            <Dropdown
              label="Internet Service"
              options={options.internetServiceOptions}
              value={formData.internetService}
              onChange={(e) => handleChange("internetService", e.target.value)}
            />
            <Dropdown
              label="Online Security"
              options={options.onlineSecurityOptions}
              value={formData.onlineSecurity}
              onChange={(e) => handleChange("onlineSecurity", e.target.value)}
            />
            <Dropdown
              label="Online Backup"
              options={options.onlineBackupOptions}
              value={formData.onlineBackup}
              onChange={(e) => handleChange("onlineBackup", e.target.value)}
            />
            <Dropdown
              label="Device Protection"
              options={options.deviceProtectionOptions}
              value={formData.deviceProtection}
              onChange={(e) => handleChange("deviceProtection", e.target.value)}
            />
            <Dropdown
              label="Tech Support"
              options={options.techSupportOptions}
              value={formData.techSupport}
              onChange={(e) => handleChange("techSupport", e.target.value)}
            />
            <Dropdown
              label="Streaming TV"
              options={options.streamingTVOptions}
              value={formData.streamingTV}
              onChange={(e) => handleChange("streamingTV", e.target.value)}
            />
            <Dropdown
              label="Streaming Movies"
              options={options.streamingMoviesOptions}
              value={formData.streamingMovies}
              onChange={(e) => handleChange("streamingMovies", e.target.value)}
            />
            <Dropdown
              label="Contract"
              options={options.contractOptions}
              value={formData.contract}
              onChange={(e) => handleChange("contract", e.target.value)}
            />
            <Dropdown
              label="Paperless Billing"
              options={options.paperlessBillingOptions}
              value={formData.paperlessBilling}
              onChange={(e) => handleChange("paperlessBilling", e.target.value)}
            />
            <Dropdown
              label="Payment Method"
              options={options.paymentMethodOptions}
              value={formData.paymentMethod}
              onChange={(e) => handleChange("paymentMethod", e.target.value)}
            />
            <NumericInput
              label="Monthly Charges"
              value={formData.monthlyCharges}
              placeholder="0.00"
              onChange={(e) => handleChange("monthlyCharges", e.target.value)}
            />
            <NumericInput
              label="Total Charges"
              value={formData.totalCharges}
              placeholder="0.00"
              onChange={(e) => handleChange("totalCharges", e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-gray-800 text-white text-sm font-medium rounded-md
                       hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2
                       disabled:bg-gray-300 disabled:cursor-not-allowed
                       transition-colors"
          >
            {loading ? "Predicting..." : "Predict Churn"}
          </button>
        </form>

        {result && (
          <div className="mt-6 p-6 bg-gray-50 border border-gray-200 rounded-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Prediction</p>
                <p className="text-2xl font-semibold text-gray-800">
                  {result.prediction === 1 ? "Will Churn" : "Will Stay"}
                </p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 mb-1">Probability</p>
                <p className="text-2xl font-semibold text-gray-800">
                  {(result.probability * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
};

export default App;
