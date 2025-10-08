import React, { useState } from "react";
import axios from "axios";

function App() {
  const API_BASE = "http://127.0.0.1:80"; // your FastAPI URL

  const [record, setRecord] = useState({
    Time_of_Booking: "Afternoon",
    Location_Category: "Urban",
    Vehicle_Type: "Economy",
    Customer_Loyalty_Status: "Regular",
    Expected_Ride_Duration: "",
    Historical_Cost_of_Ride: "",
    Number_of_Riders: "",
    Number_of_Drivers: "",
  });

  const [recommendation, setRecommendation] = useState(null);
  const [batchResult, setBatchResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [batchLoading, setBatchLoading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    const numericFields = [
      "Expected_Ride_Duration",
      "Historical_Cost_of_Ride",
      "Number_of_Riders",
      "Number_of_Drivers",
    ];
    setRecord({
      ...record,
      [name]: numericFields.includes(name) ? Number(value) : value,
    });
  };

  // Call /recommend
  const handleRecommend = async () => {
    setIsLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/recommend`, { record });
      console.log("API Response:", res.data);
      setRecommendation(res.data);
    } catch (err) {
      console.error("Error:", err);
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setIsLoading(false);
    }
  };

  // Call /recommend_batch
  const handleBatch = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFileName(file.name);
    setBatchLoading(true);
    setBatchResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("Uploading file:", file.name);
      const startTime = Date.now();
      
      const res = await axios.post(`${API_BASE}/recommend_batch`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 300000,
      });
      
      const endTime = Date.now();
      console.log(`Batch processing completed in ${((endTime - startTime) / 1000).toFixed(2)} seconds`);
      console.log("Batch Response:", res.data);
      
      setBatchResult(res.data);
    } catch (err) {
      console.error("Batch Error:", err);
      if (err.code === 'ECONNABORTED') {
        alert("Request timed out. The file might be too large or the server is taking too long to process.");
      } else {
        alert("Batch Error: " + (err.response?.data?.detail || err.message));
      }
    } finally {
      setBatchLoading(false);
    }
  };

  const getPrice = () => {
    if (!recommendation) return null;
    return recommendation.price_recommended || 
           recommendation["Price Recommended"] || 
           recommendation.price || 
           recommendation.recommended_price ||
           null;
  };

  const formatFieldName = (key) => {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatValue = (value) => {
    if (value === null || value === undefined) return "N/A";
    if (typeof value === 'object') {
      if (value.low !== undefined && value.high !== undefined) {
        return `$${value.low.toFixed(2)} - $${value.high.toFixed(2)}`;
      }
      return JSON.stringify(value);
    }
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    if (typeof value === 'boolean') {
      return value ? "Yes" : "No";
    }
    return String(value);
  };

  const getFieldColor = (key) => {
    if (key.includes("price") || key.includes("Price")) return "#10b981";
    if (key.includes("complete") || key.includes("Complete")) return "#8b5cf6";
    if (key.includes("bounds") || key.includes("Bounds")) return "#f59e0b";
    if (key.includes("gm") || key.includes("Gm")) return "#3b82f6";
    if (key.includes("baseline") || key.includes("Baseline")) return "#ef4444";
    return "#06b6d4";
  };

  const downloadResults = () => {
    if (!batchResult) return;
    const dataStr = JSON.stringify(batchResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `batch_results_${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ 
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      padding: "40px 20px",
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    }}>
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        .glass-card {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(10px);
          border-radius: 20px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          animation: fadeIn 0.6s ease-out;
        }
        .input-field, .select-field {
          width: 100%;
          padding: 12px 16px;
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          font-size: 15px;
          transition: all 0.3s ease;
          background: white;
        }
        .input-field:focus, .select-field:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
          transform: translateY(-2px);
        }
        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 14px 32px;
          border: none;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-primary:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        .stat-card {
          background: white;
          border-radius: 16px;
          padding: 20px;
          transition: all 0.3s ease;
          cursor: pointer;
          border: 2px solid transparent;
        }
        .stat-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
          border-color: #667eea;
        }
        .price-display {
          animation: pulse 2s ease-in-out infinite;
        }
      `}</style>

      <div style={{ maxWidth: "1400px", margin: "0 auto" }}>
        {/* Header */}
        <div style={{ 
          textAlign: "center", 
          marginBottom: "50px",
          animation: "float 3s ease-in-out infinite"
        }}>
          <h1 style={{ 
            fontSize: "56px", 
            color: "white", 
            margin: "0 0 10px 0",
            textShadow: "0 4px 20px rgba(0,0,0,0.2)",
            fontWeight: "800",
            letterSpacing: "-1px"
          }}>
            🚖 Dynamic Pricing
          </h1>
          <p style={{ 
            fontSize: "20px", 
            color: "rgba(255,255,255,0.9)",
            margin: 0,
            fontWeight: "300"
          }}>
            AI-Powered Ride Pricing Intelligence
          </p>
        </div>

        {/* Single Recommendation Section */}
        <div className="glass-card" style={{ padding: "40px", marginBottom: "30px" }}>
          <h2 style={{ 
            fontSize: "28px", 
            color: "#1f2937", 
            marginBottom: "30px",
            display: "flex",
            alignItems: "center",
            gap: "10px"
          }}>
            <span style={{ 
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              fontWeight: "700"
            }}>
              Single Recommendation
            </span>
          </h2>

          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "20px",
            marginBottom: "30px",
          }}>
            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                ⏰ Time of Booking
              </label>
              <select name="Time_of_Booking" value={record.Time_of_Booking} onChange={handleChange} className="select-field">
                <option>Morning</option>
                <option>Afternoon</option>
                <option>Evening</option>
                <option>Night</option>
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                📍 Location Category
              </label>
              <select name="Location_Category" value={record.Location_Category} onChange={handleChange} className="select-field">
                <option>Urban</option>
                <option>Suburban</option>
                <option>Rural</option>
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                🚗 Vehicle Type
              </label>
              <select name="Vehicle_Type" value={record.Vehicle_Type} onChange={handleChange} className="select-field">
                <option>Economy</option>
                <option>Premium</option>
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                ⭐ Loyalty Status
              </label>
              <select name="Customer_Loyalty_Status" value={record.Customer_Loyalty_Status} onChange={handleChange} className="select-field">
                <option>Regular</option>
                <option>Silver</option>
                <option>Gold</option>
              </select>
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                ⏱️ Expected Duration (min)
              </label>
              <input
                type="number"
                name="Expected_Ride_Duration"
                placeholder="e.g., 30"
                value={record.Expected_Ride_Duration}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                💰 Historical Cost ($)
              </label>
              <input
                type="number"
                name="Historical_Cost_of_Ride"
                placeholder="e.g., 25.50"
                value={record.Historical_Cost_of_Ride}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                👥 Number of Riders
              </label>
              <input
                type="number"
                name="Number_of_Riders"
                placeholder="e.g., 100"
                value={record.Number_of_Riders}
                onChange={handleChange}
                className="input-field"
              />
            </div>

            <div>
              <label style={{ display: "block", marginBottom: "8px", color: "#374151", fontWeight: "600", fontSize: "14px" }}>
                🚕 Number of Drivers
              </label>
              <input
                type="number"
                name="Number_of_Drivers"
                placeholder="e.g., 50"
                value={record.Number_of_Drivers}
                onChange={handleChange}
                className="input-field"
              />
            </div>
          </div>

          <button 
            onClick={handleRecommend} 
            disabled={isLoading}
            className="btn-primary"
          >
            {isLoading ? "🔄 Analyzing..." : "✨ Get Price Recommendation"}
          </button>

          {recommendation && (
            <div style={{
              marginTop: "40px",
              background: "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)",
              borderRadius: "20px",
              padding: "30px",
              border: "2px solid #10b981",
              animation: "fadeIn 0.5s ease-out"
            }}>
              <h3 style={{ 
                color: "#065f46", 
                marginBottom: "25px",
                fontSize: "24px",
                fontWeight: "700"
              }}>
                💡 Recommendation Result
              </h3>

              {/* Main Price */}
              <div className="price-display" style={{ 
                background: "white",
                borderRadius: "16px",
                padding: "30px",
                marginBottom: "20px",
                textAlign: "center",
                boxShadow: "0 4px 20px rgba(16, 185, 129, 0.2)"
              }}>
                <div style={{ color: "#6b7280", fontSize: "16px", marginBottom: "10px", fontWeight: "600" }}>
                  RECOMMENDED PRICE
                </div>
                <div style={{ 
                  fontSize: "64px", 
                  fontWeight: "800", 
                  background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  lineHeight: "1"
                }}>
                  ${getPrice() !== null ? Number(getPrice()).toFixed(2) : "N/A"}
                </div>
              </div>

              {/* Other Metrics */}
              <div style={{ 
                display: "grid", 
                gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                gap: "15px"
              }}>
                {Object.keys(recommendation)
                  .filter(key => key !== "price_recommended" && key !== "Price Recommended")
                  .map((key) => (
                    <div key={key} className="stat-card" style={{
                      borderLeft: `4px solid ${getFieldColor(key)}`
                    }}>
                      <div style={{ 
                        fontSize: "12px", 
                        color: "#6b7280", 
                        marginBottom: "8px",
                        fontWeight: "600",
                        textTransform: "uppercase",
                        letterSpacing: "0.5px"
                      }}>
                        {formatFieldName(key)}
                      </div>
                      <div style={{ 
                        fontSize: "22px", 
                        fontWeight: "700",
                        color: getFieldColor(key)
                      }}>
                        {formatValue(recommendation[key])}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>

        {/* Batch Recommendation Section */}
        <div className="glass-card" style={{ padding: "40px" }}>
          <h2 style={{ 
            fontSize: "28px", 
            color: "#1f2937", 
            marginBottom: "20px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            fontWeight: "700"
          }}>
            📊 Batch Recommendations
          </h2>
          
          <div style={{ display: "flex", gap: "15px", alignItems: "center", flexWrap: "wrap" }}>
            <label style={{
              flex: "1",
              minWidth: "300px",
              padding: "20px",
              border: "3px dashed #d1d5db",
              borderRadius: "16px",
              textAlign: "center",
              cursor: "pointer",
              transition: "all 0.3s ease",
              background: "white"
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = "#667eea";
              e.currentTarget.style.background = "#f9fafb";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = "#d1d5db";
              e.currentTarget.style.background = "white";
            }}>
              <input 
                type="file" 
                accept=".csv" 
                onChange={handleBatch}
                disabled={batchLoading}
                style={{ display: "none" }}
              />
              <div style={{ fontSize: "40px", marginBottom: "10px" }}>📁</div>
              <div style={{ color: "#374151", fontWeight: "600" }}>
                {uploadedFileName || "Click to upload CSV file"}
              </div>
              <div style={{ color: "#6b7280", fontSize: "14px", marginTop: "5px" }}>
                Supports CSV files up to 10MB
              </div>
            </label>

            {batchResult && (
              <button
                onClick={downloadResults}
                style={{
                  padding: "16px 28px",
                  background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                  color: "white",
                  border: "none",
                  borderRadius: "12px",
                  fontSize: "16px",
                  fontWeight: "600",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                  boxShadow: "0 4px 15px rgba(59, 130, 246, 0.4)"
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow = "0 6px 20px rgba(59, 130, 246, 0.6)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 15px rgba(59, 130, 246, 0.4)";
                }}
              >
                📥 Download Results
              </button>
            )}
          </div>

          {batchLoading && (
            <div style={{ 
              marginTop: "30px", 
              padding: "50px", 
              textAlign: "center",
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              borderRadius: "20px",
              color: "white",
              position: "relative",
              overflow: "hidden"
            }}>
              <div style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                height: "4px",
                background: "rgba(255,255,255,0.3)",
                overflow: "hidden"
              }}>
                <div style={{
                  width: "50%",
                  height: "100%",
                  background: "white",
                  animation: "shimmer 1.5s ease-in-out infinite"
                }} />
              </div>
              <div style={{ fontSize: "64px", marginBottom: "20px", animation: "float 2s ease-in-out infinite" }}>⏳</div>
              <div style={{ fontSize: "24px", fontWeight: "700", marginBottom: "10px" }}>
                Processing Your Data...
              </div>
              <div style={{ fontSize: "16px", opacity: 0.9 }}>
                {uploadedFileName}
              </div>
              <div style={{ fontSize: "14px", opacity: 0.8, marginTop: "20px" }}>
                This may take a while for large files. Please don't close this window.
              </div>
            </div>
          )}

          {batchResult && !batchLoading && (
            <div style={{ marginTop: "30px" }}>
              {/* Success Banner */}
              <div style={{
                padding: "20px",
                background: "linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)",
                borderRadius: "16px",
                marginBottom: "25px",
                border: "2px solid #28a745",
                display: "flex",
                alignItems: "center",
                gap: "15px",
                animation: "fadeIn 0.5s ease-out"
              }}>
                <div style={{ fontSize: "32px" }}>✅</div>
                <div>
                  <div style={{ fontWeight: "700", color: "#155724", fontSize: "18px" }}>
                    Processing Complete!
                  </div>
                  <div style={{ color: "#155724", fontSize: "14px" }}>
                    Your batch analysis is ready
                  </div>
                </div>
              </div>

              {/* KPI Summary */}
              {batchResult.kpis && (
                <div style={{
                  background: "linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)",
                  borderRadius: "20px",
                  padding: "30px",
                  marginBottom: "25px",
                  border: "2px solid #8b5cf6"
                }}>
                  <h3 style={{ 
                    color: "#5b21b6", 
                    marginBottom: "20px",
                    fontSize: "22px",
                    fontWeight: "700"
                  }}>
                    📊 Key Performance Indicators
                  </h3>
                  <div style={{ 
                    display: "grid", 
                    gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", 
                    gap: "15px"
                  }}>
                    {Object.keys(batchResult.kpis).map((key) => (
                      <div key={key} className="stat-card">
                        <div style={{ 
                          fontSize: "12px", 
                          color: "#6b7280", 
                          marginBottom: "8px",
                          fontWeight: "600",
                          textTransform: "uppercase"
                        }}>
                          {formatFieldName(key)}
                        </div>
                        <div style={{ 
                          fontSize: "28px", 
                          fontWeight: "800",
                          background: "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)",
                          WebkitBackgroundClip: "text",
                          WebkitTextFillColor: "transparent"
                        }}>
                          {formatValue(batchResult.kpis[key])}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Individual Recommendations */}
              {batchResult.recommendations && batchResult.recommendations.length > 0 && (
                <div>
                  <h3 style={{ 
                    color: "#1f2937", 
                    marginBottom: "20px",
                    fontSize: "22px",
                    fontWeight: "700"
                  }}>
                    📋 Individual Recommendations ({batchResult.recommendations.length} records)
                  </h3>
                  <div style={{ 
                    maxHeight: "600px", 
                    overflowY: "auto",
                    borderRadius: "16px",
                    padding: "10px",
                    background: "#f9fafb"
                  }}>
                    {batchResult.recommendations.map((rec, index) => (
                      <div
                        key={index}
                        className="stat-card"
                        style={{
                          marginBottom: "15px",
                          background: "white",
                          padding: "25px"
                        }}
                      >
                        <div style={{ 
                          fontSize: "18px",
                          fontWeight: "700",
                          color: "#1f2937",
                          marginBottom: "15px",
                          paddingBottom: "10px",
                          borderBottom: "3px solid #10b981"
                        }}>
                          #{index + 1}
                        </div>
                        <div style={{ 
                          display: "grid", 
                          gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
                          gap: "12px"
                        }}>
                          {Object.keys(rec).map((key) => (
                            <div key={key} style={{ 
                              padding: "12px",
                              background: key.includes("price") ? "#f0fdf4" : "#f9fafb",
                              borderRadius: "10px",
                              borderLeft: `3px solid ${key.includes("price") ? "#10b981" : "#d1d5db"}`
                            }}>
                              <div style={{ 
                                fontSize: "11px", 
                                color: "#6b7280",
                                marginBottom: "5px",
                                fontWeight: "600",
                                textTransform: "uppercase"
                              }}>
                                {formatFieldName(key)}
                              </div>
                              <div style={{ 
                                fontSize: "16px",
                                fontWeight: "700",
                                color: key.includes("price") ? "#10b981" : "#374151"
                              }}>
                                {formatValue(rec[key])}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
