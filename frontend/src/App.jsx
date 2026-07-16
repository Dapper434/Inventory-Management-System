import { useState, useEffect } from 'react'

function App() {
  // state to hold our items and form inputs
  const [inventory, setInventory] = useState([])
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')
  const [stock, setStock] = useState('')


 // fetch data from the backend api
  const fetchInventory = async () => {
    try {
      const response = await fetch('http://localhost:5000/inventory')
      const data = await response.json()
      setInventory(data)
    } catch (error) {
      console.error(error)
    }
  }

  // grab the list when the page first loads
  useEffect(() => {
    fetchInventory()
  }, [])















}