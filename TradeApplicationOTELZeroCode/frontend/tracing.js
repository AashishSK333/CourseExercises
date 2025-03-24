// frontend/tracing.js
function generateXrayTraceId() {
    // Format: 1-5759e988-bd862e3fe1be46a994272793
    const timestamp = Math.floor(Date.now() / 1000).toString(16);
    const randomBytes = Array.from({length: 12}, () => 
        Math.floor(Math.random() * 256).toString(16).padStart(2, '0')).join('');
    
    return `1-${timestamp.padStart(8, '0')}-${randomBytes}`;
}

function addXrayTraceHeader(headers) {
    const traceId = generateXrayTraceId();
    const parentId = Array.from({length: 8}, () => 
        Math.floor(Math.random() * 256).toString(16).padStart(2, '0')).join('');
    
    headers['X-Amzn-Trace-Id'] = `Root=1-${traceId};Parent=${parentId};Sampled=1`;
    return traceId;
}

// Expose functions to global scope
window.TraceUtil = {
    generateXrayTraceId,
    addXrayTraceHeader
};