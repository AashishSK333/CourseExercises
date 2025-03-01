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
        await submitTrade(trade);
        console.log('Trade submitted, fetching portfolio...');
        await fetchAndDisplayPortfolio(trade.trader_id);
        console.log('Portfolio fetched and displayed');
    } catch (error) {
        console.error('Error during form submission:', error);
    }
});

async function submitTrade(trade) {
    try {
        console.log('Sending POST request to trade_service...');
        const response = await fetch('/trades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(trade)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log('Trade submitted successfully');
    } catch (error) {
        console.error('Error submitting trade:', error);
        throw error;  // Re-throw the error to be caught by the outer try-catch
    }
}

async function fetchAndDisplayPortfolio(traderId) {
    try {
        console.log('Sending GET request to portfolio_service...');
        const response = await fetch(`/portfolio/${traderId}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const portfolio = await response.json();
        console.log('Portfolio data:', portfolio);
        document.getElementById('portfolio').innerHTML = JSON.stringify(portfolio, null, 2);

        console.log('Portfolio fetched and displayed successfully');
    } catch (error) {
        console.error('Error fetching portfolio:', error);
        throw error;  // Re-throw the error to be caught by the outer try-catch
    }
}