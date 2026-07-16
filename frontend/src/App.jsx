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


  // handle the form submission for adding items
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // build the item object
    const newItem = {
      name,
      price: parseFloat(price),
      stock: parseInt(stock)
    }


    try {
      // send the new item to our flask backend
      await fetch('http://localhost:5000/inventory', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newItem)
      })
      
      // clear the form after saving
      setName('')
      setPrice('')
      setStock('')
      
      // refresh the list to show the new item
      fetchInventory()
    } catch (error) {
      console.error(error)
    }
  }


  // delete an item by its id
  const handleDelete = async (id) => {
    try {
      await fetch(`http://localhost:5000/inventory/${id}`, {
        method: 'DELETE'
      })
     
      // refresh the list to remove it from the screen
      fetchInventory()
    } catch (error) {
      console.error(error)
    }


    return (
      <div className="container">
        <h1>Inventory Management System</h1>
        
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            placeholder="Product Name" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
          <input 
            type="number" 
            placeholder="Price" 
            value={price} 
            onChange={(e) => setPrice(e.target.value)} 
            required 
          />
          <input 
            type="number" 
            placeholder="Stock Quantity" 
            value={stock} 
            onChange={(e) => setStock(e.target.value)} 
            required 
          />
  
          <button type="submit">Add Item</button>
        </form>
  
        <div className="inventory-list">
          {inventory.map(item => (
            <div key={item.id} className="item-card">
              <div className="item-details">
                <h3>{item.name}</h3>
                <p>Price: ${item.price}</p>
                <p>Stock: {item.stock}</p>
                {item.brands && <p>Brand: {item.brands}</p>}
                {item.ingredients_text && <p>Ingredients: {item.ingredients_text}</p>}
              </div>
              <button className="delete-btn" onClick={() => handleDelete(item.id)}>Delete</button>
            </div>
          ))}
        </div>
      </div>
    )
  }
  
  export default App
  






}