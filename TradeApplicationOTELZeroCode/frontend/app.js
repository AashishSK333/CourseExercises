// Without ES6 imports
// Replace this line
// import { addXrayTraceHeader } from './tracing.js';

document.getElementById('tradeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Form submission started');
    
    const trade = {
        asset_name: document.getElementById('assetName').value,
        quantity: document.getElementById('quantity').value,
        price: document.getElementById('price').value,
        trade_time: document.getElementById('tradeTime').value,
        trader_id: document.getElementById('traderId').value
    };

    console.log('Trade data:', trade);

    try {
        console.log('Submitting trade...');
        
        // Create a trace ID for the entire transaction
        const traceId = generateTraceId();
        console.log('Generated trace ID:', traceId);
        
        // Store the trace ID for future calls
        sessionStorage.setItem('currentTraceId', traceId);
        
        // Submit trade with trace headers
        await submitTrade(trade, traceId);
        
        console.log('Trade submitted, fetching portfolio...');
        await fetchAndDisplayPortfolio(trade.trader_id, traceId);
        console.log('Portfolio fetched and displayed');
    } catch (error) {
        console.error('Error during form submission:', error);
    }
});

// Define this function to generate a trace ID
function generateTraceId() {
    const timestamp = Math.floor(Date.now() / 1000).toString(16);
    const randomPart = Math.random().toString(16).substring(2, 14);
    return `1-${timestamp.padStart(8, '0')}-${randomPart}`;
}

// Ensure this function actually exists and matches the call in the event listener
async function submitTrade(trade, traceId) {
    try {
        console.log('Sending POST request to trade_service');
        const response = await fetch('/trades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Amzn-Trace-Id': `Root=${traceId}`
            },
            body: JSON.stringify(trade)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log('Trade submitted successfully');
        return await response.json();
    } catch (error) {
        console.error('Error submitting trade:', error);
        throw error;
    }
}

// Make sure this function exists with this exact name
async function fetchAndDisplayPortfolio(traderId, traceId) {
    try {
        console.log(`Fetching portfolio for trader ${traderId}`);
        
        // Use the trace ID passed from the event listener
        const headers = {'X-Amzn-Trace-Id': `Root=${traceId}`};
        
        // If no trace ID was passed, try to get from session storage
        if (!traceId) {
            const storedTraceId = sessionStorage.getItem('currentTraceId');
            if (storedTraceId) {
                headers['X-Amzn-Trace-Id'] = `Root=${storedTraceId}`;
            }
        }
        
        const response = await fetch(`/portfolio/${traderId}`, {
            headers: headers
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const responseText = await response.text();
        console.log('Raw response:', responseText);
        
        if (!responseText) {
            throw new Error('Empty response from server');
        }
        
        let portfolio;
        try {
            portfolio = JSON.parse(responseText);
        } catch (e) {
            console.error('Failed to parse JSON response:', e);
            throw new Error('Response was not valid JSON');
        }
        
        console.log('Portfolio data:', portfolio);
        
        // Display the portfolio
        const portfolioDiv = document.getElementById('portfolio');
        portfolioDiv.innerHTML = '';
        
        const header = document.createElement('h2');
        header.textContent = `Portfolio for Trader ${traderId}`;
        portfolioDiv.appendChild(header);
        
        if (portfolio.positions && portfolio.positions.length > 0) {
            const table = document.createElement('table');
            table.classList.add('portfolio-table');
            
            // Create header row
            const headerRow = table.insertRow();
            ['Symbol', 'Quantity', 'Average Price', 'Current Value'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });
            
            // Create data rows
            portfolio.positions.forEach(position => {
                const row = table.insertRow();
                
                const symbolCell = row.insertCell();
                symbolCell.textContent = position.symbol;
                
                const quantityCell = row.insertCell();
                quantityCell.textContent = position.quantity;
                
                const priceCell = row.insertCell();
                priceCell.textContent = `$${parseFloat(position.average_price).toFixed(2)}`;
                
                const valueCell = row.insertCell();
                const value = position.quantity * position.average_price;
                valueCell.textContent = `$${value.toFixed(2)}`;
            });
            
            // Add total row
            const totalRow = table.insertRow();
            const totalLabelCell = totalRow.insertCell();
            totalLabelCell.textContent = 'Total Portfolio Value:';
            totalLabelCell.colSpan = 3;
            totalLabelCell.style.textAlign = 'right';
            totalLabelCell.style.fontWeight = 'bold';
            
            const totalValueCell = totalRow.insertCell();
            totalValueCell.textContent = `$${parseFloat(portfolio.total_value).toFixed(2)}`;
            totalValueCell.style.fontWeight = 'bold';
            
            portfolioDiv.appendChild(table);
        } else {
            const message = document.createElement('p');
            message.textContent = 'No positions in portfolio.';
            portfolioDiv.appendChild(message);
        }
    } catch (error) {
        console.error('Error fetching portfolio:', error);
        const portfolioDiv = document.getElementById('portfolio');
        portfolioDiv.innerHTML = `<p class="error">Error loading portfolio: ${error.message}</p>`;
    }
}