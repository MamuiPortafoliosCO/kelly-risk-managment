//+------------------------------------------------------------------+
//|                                                    Communication.mqh |
//|                        RiskOptima Engine - MQL5/Python Communication |
//|                        https://github.com/your-repo/risk-optima-engine |
//+------------------------------------------------------------------+
#property copyright "RiskOptima Engine Team"
#property link      "https://github.com/your-repo/risk-optima-engine"
#property version   "1.1.0"
#property strict

// Communication protocol constants
#define COMM_PROTOCOL_VERSION    "1.0"
#define COMM_MAX_MESSAGE_SIZE    4096
#define COMM_TIMEOUT_SECONDS     30
#define COMM_RETRY_ATTEMPTS      3
#define COMM_RETRY_DELAY_MS      1000

// Communication channels
enum ENUM_COMM_CHANNEL
{
    COMM_CHANNEL_FILE,        // File-based communication
    COMM_CHANNEL_SHARED_MEM,  // Shared memory (future)
    COMM_CHANNEL_SOCKET,      // Network socket (future)
    COMM_CHANNEL_NAMED_PIPE   // Named pipe (future)
};

// Message types
enum ENUM_COMM_MESSAGE_TYPE
{
    COMM_MSG_TRADE_SIGNAL,      // Trading signal from MQL5 to Python
    COMM_MSG_RISK_UPDATE,       // Risk metrics update
    COMM_MSG_CONFIG_UPDATE,     // Configuration update
    COMM_MSG_STATUS_REQUEST,    // Status request
    COMM_MSG_STATUS_RESPONSE,   // Status response
    COMM_MSG_ERROR,             // Error message
    COMM_MSG_HEARTBEAT,         // Heartbeat/keepalive
    COMM_MSG_SYNC_REQUEST,      // Synchronization request
    COMM_MSG_SYNC_RESPONSE      // Synchronization response
};

// Communication status
enum ENUM_COMM_STATUS
{
    COMM_STATUS_DISCONNECTED,
    COMM_STATUS_CONNECTING,
    COMM_STATUS_CONNECTED,
    COMM_STATUS_ERROR,
    COMM_STATUS_TIMEOUT
};

//+------------------------------------------------------------------+
//| Communication Message Structure                                  |
//+------------------------------------------------------------------+
struct CommMessage
{
    string              protocol_version;
    ENUM_COMM_MESSAGE_TYPE message_type;
    datetime            timestamp;
    string              sender_id;
    string              message_id;
    string              payload;
    int                 sequence_number;
    string              checksum;

    // Default constructor
    CommMessage()
    {
        protocol_version = COMM_PROTOCOL_VERSION;
        timestamp = TimeCurrent();
        sequence_number = 0;
        checksum = "";
    }
};

//+------------------------------------------------------------------+
//| Communication Manager Class                                      |
//+------------------------------------------------------------------+
class CCommunicationManager
{
private:
    ENUM_COMM_CHANNEL   m_channel;
    ENUM_COMM_STATUS    m_status;
    string              m_comm_path;
    string              m_session_id;
    int                 m_sequence_counter;
    datetime            m_last_heartbeat;
    int                 m_heartbeat_interval;

    // File-based communication
    string              m_inbox_file;
    string              m_outbox_file;
    string              m_status_file;

public:
                     CCommunicationManager();
                    ~CCommunicationManager();

    // Initialization
    bool              Initialize(ENUM_COMM_CHANNEL channel = COMM_CHANNEL_FILE);
    void              Shutdown();

    // Connection management
    bool              Connect();
    void              Disconnect();
    ENUM_COMM_STATUS  GetStatus() const { return m_status; }

    // Message handling
    bool              SendMessage(ENUM_COMM_MESSAGE_TYPE msg_type, string payload);
    bool              ReceiveMessage(CommMessage &message);
    bool              SendHeartbeat();
    bool              CheckHeartbeat();

    // Configuration
    void              SetHeartbeatInterval(int seconds) { m_heartbeat_interval = seconds; }
    void              SetCommPath(string path) { m_comm_path = path; }

private:
    // File-based communication methods
    bool              InitFileCommunication();
    bool              SendMessageFile(const CommMessage &message);
    bool              ReceiveMessageFile(CommMessage &message);
    bool              WriteMessageToFile(string filename, const CommMessage &message);
    bool              ReadMessageFromFile(string filename, CommMessage &message);

    // Utility methods
    string            GenerateMessageId();
    string            CalculateChecksum(const CommMessage &message);
    bool              ValidateMessage(const CommMessage &message);
    string            MessageTypeToString(ENUM_COMM_MESSAGE_TYPE msg_type);
    ENUM_COMM_MESSAGE_TYPE StringToMessageType(string type_str);

    // File operations
    bool              EnsureDirectoryExists(string path);
    bool              FileExists(string filename);
    bool              DeleteFile(string filename);
    datetime          GetFileModificationTime(string filename);
};

//+------------------------------------------------------------------+
//| Constructor                                                      |
//+------------------------------------------------------------------+
CCommunicationManager::CCommunicationManager()
{
    m_channel = COMM_CHANNEL_FILE;
    m_status = COMM_STATUS_DISCONNECTED;
    m_sequence_counter = 0;
    m_last_heartbeat = 0;
    m_heartbeat_interval = 60; // 1 minute default

    // Generate unique session ID
    m_session_id = StringFormat("MQL5_%d_%d", AccountInfoInteger(ACCOUNT_LOGIN), TimeCurrent());
}

//+------------------------------------------------------------------+
//| Destructor                                                       |
//+------------------------------------------------------------------+
CCommunicationManager::~CCommunicationManager()
{
    Shutdown();
}

//+------------------------------------------------------------------+
//| Initialize communication manager                                 |
//+------------------------------------------------------------------+
bool CCommunicationManager::Initialize(ENUM_COMM_CHANNEL channel)
{
    m_channel = channel;

    // Set default communication path
    if (m_comm_path == "")
    {
        m_comm_path = TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files\\RiskOptima\\";
    }

    // Initialize based on channel type
    bool result = false;
    switch (m_channel)
    {
        case COMM_CHANNEL_FILE:
            result = InitFileCommunication();
            break;
        default:
            Print("Unsupported communication channel");
            return false;
    }

    if (result)
    {
        m_status = COMM_STATUS_DISCONNECTED;
        Print("Communication manager initialized successfully");
    }

    return result;
}

//+------------------------------------------------------------------+
//| Shutdown communication manager                                   |
//+------------------------------------------------------------------+
void CCommunicationManager::Shutdown()
{
    Disconnect();
    Print("Communication manager shutdown");
}

//+------------------------------------------------------------------+
//| Initialize file-based communication                               |
//+------------------------------------------------------------------+
bool CCommunicationManager::InitFileCommunication()
{
    // Ensure communication directory exists
    if (!EnsureDirectoryExists(m_comm_path))
    {
        Print("Failed to create communication directory: ", m_comm_path);
        return false;
    }

    // Set up file paths
    m_inbox_file = m_comm_path + "inbox_" + m_session_id + ".json";
    m_outbox_file = m_comm_path + "outbox_" + m_session_id + ".json";
    m_status_file = m_comm_path + "status_" + m_session_id + ".json";

    Print("File-based communication initialized:");
    Print("  Inbox: ", m_inbox_file);
    Print("  Outbox: ", m_outbox_file);
    Print("  Status: ", m_status_file);

    return true;
}

//+------------------------------------------------------------------+
//| Connect to communication channel                                 |
//+------------------------------------------------------------------+
bool CCommunicationManager::Connect()
{
    if (m_status == COMM_STATUS_CONNECTED)
        return true;

    m_status = COMM_STATUS_CONNECTING;

    // For file-based communication, just check if we can write to the directory
    if (m_channel == COMM_CHANNEL_FILE)
    {
        // Try to write a test file
        string test_file = m_comm_path + "test_connection.tmp";
        int handle = FileOpen(test_file, FILE_WRITE | FILE_TXT);
        if (handle != INVALID_HANDLE)
        {
            FileWrite(handle, "connection_test");
            FileClose(handle);

            // Clean up test file
            FileDelete(test_file);

            m_status = COMM_STATUS_CONNECTED;
            m_last_heartbeat = TimeCurrent();
            Print("Connected to communication channel");
            return true;
        }
        else
        {
            m_status = COMM_STATUS_ERROR;
            Print("Failed to connect to communication channel");
            return false;
        }
    }

    return false;
}

//+------------------------------------------------------------------+
//| Disconnect from communication channel                            |
//+------------------------------------------------------------------+
void CCommunicationManager::Disconnect()
{
    m_status = COMM_STATUS_DISCONNECTED;

    // Clean up files if needed
    if (m_channel == COMM_CHANNEL_FILE)
    {
        // Optionally clean up old message files
        // FileDelete(m_inbox_file);
        // FileDelete(m_outbox_file);
    }

    Print("Disconnected from communication channel");
}

//+------------------------------------------------------------------+
//| Send message                                                     |
//+------------------------------------------------------------------+
bool CCommunicationManager::SendMessage(ENUM_COMM_MESSAGE_TYPE msg_type, string payload)
{
    if (m_status != COMM_STATUS_CONNECTED)
    {
        if (!Connect())
            return false;
    }

    CommMessage message;
    message.message_type = msg_type;
    message.sender_id = m_session_id;
    message.message_id = GenerateMessageId();
    message.payload = payload;
    message.sequence_number = ++m_sequence_counter;
    message.checksum = CalculateChecksum(message);

    bool result = false;
    switch (m_channel)
    {
        case COMM_CHANNEL_FILE:
            result = SendMessageFile(message);
            break;
    }

    if (result)
    {
        Print("Message sent: ", MessageTypeToString(msg_type));
    }
    else
    {
        Print("Failed to send message: ", MessageTypeToString(msg_type));
    }

    return result;
}

//+------------------------------------------------------------------+
//| Receive message                                                  |
//+------------------------------------------------------------------+
bool CCommunicationManager::ReceiveMessage(CommMessage &message)
{
    if (m_status != COMM_STATUS_CONNECTED)
        return false;

    bool result = false;
    switch (m_channel)
    {
        case COMM_CHANNEL_FILE:
            result = ReceiveMessageFile(message);
            break;
    }

    return result;
}

//+------------------------------------------------------------------+
//| Send heartbeat                                                   |
//+------------------------------------------------------------------+
bool CCommunicationManager::SendHeartbeat()
{
    string payload = StringFormat("{\"timestamp\":%d,\"status\":\"active\"}", TimeCurrent());
    return SendMessage(COMM_MSG_HEARTBEAT, payload);
}

//+------------------------------------------------------------------+
//| Check heartbeat status                                           |
//+------------------------------------------------------------------+
bool CCommunicationManager::CheckHeartbeat()
{
    if (TimeCurrent() - m_last_heartbeat > m_heartbeat_interval)
    {
        if (!SendHeartbeat())
        {
            m_status = COMM_STATUS_ERROR;
            return false;
        }
        m_last_heartbeat = TimeCurrent();
    }
    return true;
}

//+------------------------------------------------------------------+
//| Send message via file                                            |
//+------------------------------------------------------------------+
bool CCommunicationManager::SendMessageFile(const CommMessage &message)
{
    return WriteMessageToFile(m_outbox_file, message);
}

//+------------------------------------------------------------------+
//| Receive message via file                                         |
//+------------------------------------------------------------------+
bool CCommunicationManager::ReceiveMessageFile(CommMessage &message)
{
    return ReadMessageFromFile(m_inbox_file, message);
}

//+------------------------------------------------------------------+
//| Write message to file                                            |
//+------------------------------------------------------------------+
bool CCommunicationManager::WriteMessageToFile(string filename, const CommMessage &message)
{
    int handle = FileOpen(filename, FILE_WRITE | FILE_TXT | FILE_ANSI);
    if (handle == INVALID_HANDLE)
    {
        Print("Failed to open file for writing: ", filename);
        return false;
    }

    // Create JSON-like structure
    string json = "{";
    json += "\"protocol_version\":\"" + message.protocol_version + "\",";
    json += "\"message_type\":\"" + MessageTypeToString(message.message_type) + "\",";
    json += "\"timestamp\":" + IntegerToString(message.timestamp) + ",";
    json += "\"sender_id\":\"" + message.sender_id + "\",";
    json += "\"message_id\":\"" + message.message_id + "\",";
    json += "\"payload\":\"" + message.payload + "\",";
    json += "\"sequence_number\":" + IntegerToString(message.sequence_number) + ",";
    json += "\"checksum\":\"" + message.checksum + "\"";
    json += "}";

    uint bytes_written = FileWrite(handle, json);
    FileClose(handle);

    if (bytes_written == 0)
    {
        Print("Failed to write message to file: ", filename);
        return false;
    }

    return true;
}

//+------------------------------------------------------------------+
//| Read message from file                                           |
//+------------------------------------------------------------------+
bool CCommunicationManager::ReadMessageFromFile(string filename, CommMessage &message)
{
    if (!FileExists(filename))
        return false;

    int handle = FileOpen(filename, FILE_READ | FILE_TXT | FILE_ANSI);
    if (handle == INVALID_HANDLE)
        return false;

    string json = FileReadString(handle);
    FileClose(handle);

    if (json == "")
        return false;

    // Simple JSON parsing (in production, use a proper JSON parser)
    // This is a simplified implementation

    // Extract message type
    string msg_type_str = ExtractJsonValue(json, "message_type");
    message.message_type = StringToMessageType(msg_type_str);

    // Extract other fields
    message.protocol_version = ExtractJsonValue(json, "protocol_version");
    message.timestamp = (datetime)StringToInteger(ExtractJsonValue(json, "timestamp"));
    message.sender_id = ExtractJsonValue(json, "sender_id");
    message.message_id = ExtractJsonValue(json, "message_id");
    message.payload = ExtractJsonValue(json, "payload");
    message.sequence_number = (int)StringToInteger(ExtractJsonValue(json, "sequence_number"));
    message.checksum = ExtractJsonValue(json, "checksum");

    // Validate message
    if (!ValidateMessage(message))
    {
        Print("Message validation failed");
        return false;
    }

    // Delete file after successful read
    FileDelete(filename);

    return true;
}

//+------------------------------------------------------------------+
//| Extract value from JSON string (simplified)                      |
//+------------------------------------------------------------------+
string ExtractJsonValue(string json, string key)
{
    string search = "\"" + key + "\":";
    int start_pos = StringFind(json, search);

    if (start_pos == -1)
        return "";

    start_pos += StringLen(search);

    // Handle quoted strings
    if (StringSubstr(json, start_pos, 1) == "\"")
    {
        start_pos++; // Skip opening quote
        int end_pos = StringFind(json, "\"", start_pos);
        if (end_pos == -1)
            return "";
        return StringSubstr(json, start_pos, end_pos - start_pos);
    }
    // Handle numbers
    else
    {
        int end_pos = StringFind(json, ",", start_pos);
        if (end_pos == -1)
            end_pos = StringFind(json, "}", start_pos);
        if (end_pos == -1)
            return "";
        return StringSubstr(json, start_pos, end_pos - start_pos);
    }
}

//+------------------------------------------------------------------+
//| Generate unique message ID                                       |
//+------------------------------------------------------------------+
string CCommunicationManager::GenerateMessageId()
{
    return StringFormat("MSG_%d_%d", TimeCurrent(), m_sequence_counter);
}

//+------------------------------------------------------------------+
//| Calculate message checksum                                       |
//+------------------------------------------------------------------+
string CCommunicationManager::CalculateChecksum(const CommMessage &message)
{
    string data = message.sender_id + IntegerToString(message.timestamp) +
                  message.payload + IntegerToString(message.sequence_number);

    // Simple checksum (in production, use proper hashing)
    int sum = 0;
    for (int i = 0; i < StringLen(data); i++)
    {
        sum += StringGetCharacter(data, i);
    }

    return IntegerToString(sum);
}

//+------------------------------------------------------------------+
//| Validate message                                                 |
//+------------------------------------------------------------------+
bool CCommunicationManager::ValidateMessage(const CommMessage &message)
{
    // Check protocol version
    if (message.protocol_version != COMM_PROTOCOL_VERSION)
        return false;

    // Check checksum
    string expected_checksum = CalculateChecksum(message);
    if (message.checksum != expected_checksum)
        return false;

    // Check timestamp (not too old)
    if (TimeCurrent() - message.timestamp > 300) // 5 minutes
        return false;

    return true;
}

//+------------------------------------------------------------------+
//| Convert message type to string                                   |
//+------------------------------------------------------------------+
string CCommunicationManager::MessageTypeToString(ENUM_COMM_MESSAGE_TYPE msg_type)
{
    switch (msg_type)
    {
        case COMM_MSG_TRADE_SIGNAL: return "trade_signal";
        case COMM_MSG_RISK_UPDATE: return "risk_update";
        case COMM_MSG_CONFIG_UPDATE: return "config_update";
        case COMM_MSG_STATUS_REQUEST: return "status_request";
        case COMM_MSG_STATUS_RESPONSE: return "status_response";
        case COMM_MSG_ERROR: return "error";
        case COMM_MSG_HEARTBEAT: return "heartbeat";
        case COMM_MSG_SYNC_REQUEST: return "sync_request";
        case COMM_MSG_SYNC_RESPONSE: return "sync_response";
        default: return "unknown";
    }
}

//+------------------------------------------------------------------+
//| Convert string to message type                                   |
//+------------------------------------------------------------------+
ENUM_COMM_MESSAGE_TYPE CCommunicationManager::StringToMessageType(string type_str)
{
    if (type_str == "trade_signal") return COMM_MSG_TRADE_SIGNAL;
    if (type_str == "risk_update") return COMM_MSG_RISK_UPDATE;
    if (type_str == "config_update") return COMM_MSG_CONFIG_UPDATE;
    if (type_str == "status_request") return COMM_MSG_STATUS_REQUEST;
    if (type_str == "status_response") return COMM_MSG_STATUS_RESPONSE;
    if (type_str == "error") return COMM_MSG_ERROR;
    if (type_str == "heartbeat") return COMM_MSG_HEARTBEAT;
    if (type_str == "sync_request") return COMM_MSG_SYNC_REQUEST;
    if (type_str == "sync_response") return COMM_MSG_SYNC_RESPONSE;
    return COMM_MSG_ERROR;
}

//+------------------------------------------------------------------+
//| Ensure directory exists                                          |
//+------------------------------------------------------------------+
bool CCommunicationManager::EnsureDirectoryExists(string path)
{
    // MQL5 doesn't have direct directory creation functions
    // This is a simplified check - in practice, you might need
    // to create directories through external means

    // For now, just check if we can write to the path
    string test_file = path + "test.tmp";
    int handle = FileOpen(test_file, FILE_WRITE | FILE_TXT);
    if (handle != INVALID_HANDLE)
    {
        FileClose(handle);
        FileDelete(test_file);
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Check if file exists                                             |
//+------------------------------------------------------------------+
bool CCommunicationManager::FileExists(string filename)
{
    int handle = FileOpen(filename, FILE_READ | FILE_TXT);
    if (handle != INVALID_HANDLE)
    {
        FileClose(handle);
        return true;
    }
    return false;
}

//+------------------------------------------------------------------+
//| Delete file                                                      |
//+------------------------------------------------------------------+
bool CCommunicationManager::DeleteFile(string filename)
{
    return FileDelete(filename);
}

//+------------------------------------------------------------------+
//| Get file modification time                                       |
//+------------------------------------------------------------------+
datetime CCommunicationManager::GetFileModificationTime(string filename)
{
    // MQL5 doesn't provide direct file modification time
    // This is a placeholder
    return 0;
}

//+------------------------------------------------------------------+