import { useState } from 'react'
import axios from 'axios'

// Use proxy for local development, direct URL for production
const API_URL = import.meta.env.DEV ? '/api' : 'https://car-classifier-tilhbeahgq-uc.a.run.app'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleImageSelect = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedImage(file)
      setError(null)
      setResults(null)

      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const classifyImage = async () => {
    if (!selectedImage) return

    setLoading(true)
    setError(null)

    try {
      const reader = new FileReader()
      reader.onloadend = async () => {
        const base64Image = reader.result.split(',')[1]

        try {
          const [bodyTypeResponse, brandResponse] = await Promise.all([
            axios.post(`${API_URL}/predict/body-type`, { image: base64Image }),
            axios.post(`${API_URL}/predict/brand`, { image: base64Image })
          ])

          setResults({
            bodyType: bodyTypeResponse.data,
            brand: brandResponse.data
          })
        } catch (err) {
          console.error('API Error:', err)
          setError(err.response?.data?.detail || 'Failed to classify image. Please try again.')
        } finally {
          setLoading(false)
        }
      }
      reader.readAsDataURL(selectedImage)
    } catch (err) {
      console.error('Error:', err)
      setError('Failed to process image. Please try again.')
      setLoading(false)
    }
  }

  const reset = () => {
    setSelectedImage(null)
    setImagePreview(null)
    setResults(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <header className="bg-turners-blue text-white shadow-lg">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">Turners Insurance</h1>
          <p className="text-blue-100 mt-1">AI-Powered Vehicle Classification</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-xl overflow-hidden">
          {/* Info Banner */}
          <div className="bg-blue-600 text-white px-6 py-4">
            <h2 className="text-xl font-semibold">Quick Vehicle Assessment</h2>
            <p className="text-sm text-blue-100 mt-1">
              Upload a photo of your vehicle to get instant classification powered by AI
            </p>
          </div>

          <div className="p-6 space-y-6">
            {/* Upload Section */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Vehicle Photo
              </label>
              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    {imagePreview ? (
                      <img
                        src={imagePreview}
                        alt="Preview"
                        className="max-h-52 object-contain"
                      />
                    ) : (
                      <>
                        <svg className="w-12 h-12 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p className="mb-2 text-sm text-gray-500">
                          <span className="font-semibold">Click to upload</span> or drag and drop
                        </p>
                        <p className="text-xs text-gray-500">PNG, JPG or JPEG (MAX. 10MB)</p>
                      </>
                    )}
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleImageSelect}
                  />
                </label>
              </div>
            </div>

            {/* Action Buttons */}
            {selectedImage && (
              <div className="flex gap-3">
                <button
                  onClick={classifyImage}
                  disabled={loading}
                  className="flex-1 bg-turners-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Classifying...
                    </span>
                  ) : (
                    'Classify Vehicle'
                  )}
                </button>
                <button
                  onClick={reset}
                  className="px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition"
                >
                  Reset
                </button>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <p className="ml-3 text-sm text-red-700">{error}</p>
                </div>
              </div>
            )}

            {/* Results Section */}
            {results && (
              <div className="space-y-4 border-t pt-6">
                <h3 className="text-xl font-bold text-gray-800">Classification Results</h3>

                {/* Body Type */}
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-700">Vehicle Type</h4>
                    <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                      {(results.bodyType.confidence * 100).toFixed(1)}% Confident
                    </span>
                  </div>
                  <p className="text-2xl font-bold text-green-900">
                    {results.bodyType.predicted_class}
                  </p>
                  <div className="mt-3 text-sm text-gray-600">
                    <p className="font-medium mb-1">Top 3 Predictions:</p>
                    {results.bodyType.top_3_predictions.map((pred, idx) => (
                      <div key={idx} className="flex justify-between py-1">
                        <span>{pred.class}</span>
                        <span className="text-gray-500">{(pred.confidence * 100).toFixed(2)}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Brand */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-700">Vehicle Brand</h4>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                      {(results.brand.confidence * 100).toFixed(1)}% Confident
                    </span>
                  </div>
                  <p className="text-2xl font-bold text-blue-900">
                    {results.brand.predicted_class}
                  </p>
                  <div className="mt-3 text-sm text-gray-600">
                    <p className="font-medium mb-1">Top 5 Predictions:</p>
                    {results.brand.top_5_predictions.map((pred, idx) => (
                      <div key={idx} className="flex justify-between py-1">
                        <span>{pred.class}</span>
                        <span className="text-gray-500">{(pred.confidence * 100).toFixed(2)}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Insurance Info */}
                <div className="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
                  <h4 className="font-semibold text-gray-700 mb-2">📊 Risk Assessment</h4>
                  <p className="text-sm text-gray-600">
                    Based on the vehicle classification, our team can provide you with an accurate insurance quote.
                    Vehicle type and brand are key factors in determining insurance premiums.
                  </p>
                  <button className="mt-3 w-full bg-turners-red text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition">
                    Get Full Insurance Quote →
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>
            Powered by AI | Hosted on Azure Static Web Apps | ML API on Google Cloud Platform
          </p>
          <p className="mt-1 text-xs text-gray-500">
            Accuracy: Body Type 97.6% | Brand 75.2% | Trained on 23,000+ images
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
