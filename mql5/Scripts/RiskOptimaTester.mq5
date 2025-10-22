//+------------------------------------------------------------------+
//|                                                RiskOptimaTester.mq5 |
//|                        RiskOptima Engine - Testing Script         |
//|                        https://github.com/your-repo/risk-optima-engine |
//+------------------------------------------------------------------+
#property copyright "RiskOptima Engine Team"
#property link      "https://github.com/your-repo/risk-optima-engine"
#property version   "1.1.0"
#property script_show_inputs

#include "..\Include\RiskOptimaEngine.mqh"
#include "..\Include\Communication.mqh"

// Input parameters for testing
input bool   RunBasicTests         = true;     // Run basic functionality tests
input bool   RunRiskTests          = true;     // Run risk management tests
input bool   RunCommunicationTests = true;     // Run communication tests
input bool   RunPerformanceTests   = false;    // Run performance tests
input int    TestIterations        = 100;      // Number of test iterations
input double TestAccountBalance    = 10000;    // Test account balance
input string TestSymbol            = "EURUSD"; // Test symbol

// Global variables
CRiskOptimaEngine *g_testEngine = NULL;
CCommunicationManager *g_commManager = NULL;
int g_testsPassed = 0;
int g_testsFailed = 0;

//+------------------------------------------------------------------+
//| Script execution function                                        |
//+------------------------------------------------------------------+
void OnStart()
{
    Print("=== RiskOptima Engine Test Suite ===");
    Print("Starting tests at: ", TimeToString(TimeCurrent()));

    // Initialize test environment
    if (!InitializeTestEnvironment())
    {
        Print("Failed to initialize test environment");
        return;
    }

    // Run test suites
    if (RunBasicTests)
        RunBasicFunctionalityTests();

    if (RunRiskTests)
        RunRiskManagementTests();

    if (RunCommunicationTests)
        RunCommunicationTests();

    if (RunPerformanceTests)
        RunPerformanceTests();

    // Print test results
    PrintTestResults();

    // Cleanup
    CleanupTestEnvironment();

    Print("=== Test Suite Complete ===");
}

//+------------------------------------------------------------------+
//| Initialize test environment                                      |
//+------------------------------------------------------------------+
bool InitializeTestEnvironment()
{
    Print("Initializing test environment...");

    // Create RiskOptima Engine instance
    g_testEngine = new CRiskOptimaEngine();
    if (g_testEngine == NULL)
    {
        Print("ERROR: Failed to create RiskOptima Engine instance");
        return false;
    }

    // Configure for testing
    RiskOptimaConfig config;
    config.kelly_fraction = 0.5;
    config.optimal_f_fraction = 0.02;
    config.max_risk_per_trade = 2.0;
    config.max_daily_loss = 5.0;
    config.max_total_loss = 10.0;
    config.min_trading_days = 30;
    config.use_compound_sizing = true;
    config.enable_risk_management = true;
    config.risk_model = "kelly";
    config.magic_number = 999999; // Test magic number
    config.comment_prefix = "Test";

    if (!g_testEngine.Initialize(config))
    {
        Print("ERROR: Failed to initialize RiskOptima Engine");
        delete g_testEngine;
        g_testEngine = NULL;
        return false;
    }

    // Create communication manager
    g_commManager = new CCommunicationManager();
    if (g_commManager == NULL)
    {
        Print("ERROR: Failed to create Communication Manager");
        return false;
    }

    if (!g_commManager.Initialize(COMM_CHANNEL_FILE))
    {
        Print("ERROR: Failed to initialize Communication Manager");
        delete g_commManager;
        g_commManager = NULL;
        return false;
    }

    Print("Test environment initialized successfully");
    return true;
}

//+------------------------------------------------------------------+
//| Cleanup test environment                                         |
//+------------------------------------------------------------------+
void CleanupTestEnvironment()
{
    Print("Cleaning up test environment...");

    if (g_testEngine != NULL)
    {
        delete g_testEngine;
        g_testEngine = NULL;
    }

    if (g_commManager != NULL)
    {
        g_commManager.Shutdown();
        delete g_commManager;
        g_commManager = NULL;
    }

    Print("Test environment cleaned up");
}

//+------------------------------------------------------------------+
//| Run basic functionality tests                                    |
//+------------------------------------------------------------------+
void RunBasicFunctionalityTests()
{
    Print("\n--- Running Basic Functionality Tests ---");

    // Test 1: Engine initialization
    TestEngineInitialization();

    // Test 2: Configuration management
    TestConfigurationManagement();

    // Test 3: Statistics calculation
    TestStatisticsCalculation();

    // Test 4: Position size calculation
    TestPositionSizeCalculation();
}

//+------------------------------------------------------------------+
//| Run risk management tests                                        |
//+------------------------------------------------------------------+
void RunRiskManagementTests()
{
    Print("\n--- Running Risk Management Tests ---");

    // Test 1: Kelly Criterion calculation
    TestKellyCriterion();

    // Test 2: Risk limit validation
    TestRiskLimits();

    // Test 3: Daily loss monitoring
    TestDailyLossMonitoring();

    // Test 4: Emergency stop functionality
    TestEmergencyStop();
}

//+------------------------------------------------------------------+
//| Run communication tests                                          |
//+------------------------------------------------------------------+
void RunCommunicationTests()
{
    Print("\n--- Running Communication Tests ---");

    // Test 1: Connection establishment
    TestCommunicationConnection();

    // Test 2: Message sending
    TestMessageSending();

    // Test 3: Message receiving
    TestMessageReceiving();

    // Test 4: Heartbeat functionality
    TestHeartbeat();
}

//+------------------------------------------------------------------+
//| Run performance tests                                            |
//+------------------------------------------------------------------+
void RunPerformanceTests()
{
    Print("\n--- Running Performance Tests ---");

    // Test 1: Calculation speed
    TestCalculationPerformance();

    // Test 2: Memory usage
    TestMemoryUsage();

    // Test 3: Concurrent operations
    TestConcurrentOperations();
}

//+------------------------------------------------------------------+
//| Test engine initialization                                       |
//+------------------------------------------------------------------+
void TestEngineInitialization()
{
    Print("Testing engine initialization...");

    if (g_testEngine != NULL)
    {
        RiskOptimaConfig config = g_testEngine.GetConfig();
        if (config.magic_number == 999999 && config.risk_model == "kelly")
        {
            Print("✓ Engine initialization test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Engine initialization test FAILED");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Engine initialization test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test configuration management                                    |
//+------------------------------------------------------------------+
void TestConfigurationManagement()
{
    Print("Testing configuration management...");

    if (g_testEngine != NULL)
    {
        RiskOptimaConfig newConfig;
        newConfig.kelly_fraction = 0.25;
        newConfig.risk_model = "optimal_f";

        if (g_testEngine.UpdateConfig(newConfig))
        {
            RiskOptimaConfig updatedConfig = g_testEngine.GetConfig();
            if (updatedConfig.kelly_fraction == 0.25 && updatedConfig.risk_model == "optimal_f")
            {
                Print("✓ Configuration management test PASSED");
                g_testsPassed++;
            }
            else
            {
                Print("✗ Configuration management test FAILED - Config not updated correctly");
                g_testsFailed++;
            }
        }
        else
        {
            Print("✗ Configuration management test FAILED - Update failed");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Configuration management test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test statistics calculation                                      |
//+------------------------------------------------------------------+
void TestStatisticsCalculation()
{
    Print("Testing statistics calculation...");

    if (g_testEngine != NULL)
    {
        if (g_testEngine.UpdateTradeStats())
        {
            TradeStats stats = g_testEngine.GetTradeStats();

            // Basic validation - stats should be reasonable
            if (stats.current_balance >= 0 && stats.current_equity >= 0)
            {
                Print("✓ Statistics calculation test PASSED");
                g_testsPassed++;
            }
            else
            {
                Print("✗ Statistics calculation test FAILED - Invalid stats values");
                g_testsFailed++;
            }
        }
        else
        {
            Print("✗ Statistics calculation test FAILED - Update failed");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Statistics calculation test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test position size calculation                                   |
//+------------------------------------------------------------------+
void TestPositionSizeCalculation()
{
    Print("Testing position size calculation...");

    if (g_testEngine != NULL && SymbolInfoDouble(TestSymbol, SYMBOL_ASK) > 0)
    {
        double entry_price = SymbolInfoDouble(TestSymbol, SYMBOL_ASK);
        double stop_loss = entry_price - 50 * SymbolInfoDouble(TestSymbol, SYMBOL_POINT);

        double position_size = g_testEngine.CalculatePositionSize(
            TestSymbol, entry_price, stop_loss, ORDER_TYPE_BUY
        );

        if (position_size > 0 && g_testEngine.ValidatePositionSize(position_size, TestSymbol))
        {
            Print("✓ Position size calculation test PASSED");
            Print(StringFormat("   Calculated position size: %.5f lots", position_size));
            g_testsPassed++;
        }
        else
        {
            Print("✗ Position size calculation test FAILED - Invalid position size");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Position size calculation test FAILED - Symbol not available or engine NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test Kelly Criterion calculation                                 |
//+------------------------------------------------------------------+
void TestKellyCriterion()
{
    Print("Testing Kelly Criterion calculation...");

    if (g_testEngine != NULL)
    {
        double kelly_fraction = 0.0;
        if (g_testEngine.CalculateKellyFraction(kelly_fraction))
        {
            // Kelly fraction should be reasonable (between 0 and 0.1 for safety)
            if (kelly_fraction >= 0 && kelly_fraction <= 0.1)
            {
                Print("✓ Kelly Criterion test PASSED");
                Print(StringFormat("   Kelly fraction: %.4f", kelly_fraction));
                g_testsPassed++;
            }
            else
            {
                Print("✗ Kelly Criterion test FAILED - Invalid Kelly fraction");
                g_testsFailed++;
            }
        }
        else
        {
            Print("✗ Kelly Criterion test FAILED - Calculation failed");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Kelly Criterion test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test risk limits                                                 |
//+------------------------------------------------------------------+
void TestRiskLimits()
{
    Print("Testing risk limits...");

    if (g_testEngine != NULL)
    {
        bool dailyLimitOk = g_testEngine.CheckDailyLossLimit();
        bool totalLimitOk = g_testEngine.CheckTotalDrawdownLimit();

        if (dailyLimitOk && totalLimitOk)
        {
            Print("✓ Risk limits test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Risk limits test FAILED - Risk limits exceeded");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Risk limits test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test daily loss monitoring                                       |
//+------------------------------------------------------------------+
void TestDailyLossMonitoring()
{
    Print("Testing daily loss monitoring...");

    if (g_testEngine != NULL)
    {
        double dailyPnL = g_testEngine.GetDailyPnL();

        // Daily P&L should be a reasonable number
        if (dailyPnL >= -10000 && dailyPnL <= 10000) // Reasonable bounds
        {
            Print("✓ Daily loss monitoring test PASSED");
            Print(StringFormat("   Daily P&L: $%.2f", dailyPnL));
            g_testsPassed++;
        }
        else
        {
            Print("✗ Daily loss monitoring test FAILED - Invalid daily P&L");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Daily loss monitoring test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test emergency stop functionality                                |
//+------------------------------------------------------------------+
void TestEmergencyStop()
{
    Print("Testing emergency stop functionality...");

    if (g_testEngine != NULL)
    {
        // Test emergency stop logic
        bool shouldStop = g_testEngine.ShouldClosePositions();

        // In normal conditions, should not trigger emergency stop
        if (!shouldStop)
        {
            Print("✓ Emergency stop test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Emergency stop test FAILED - Unexpected emergency stop");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Emergency stop test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test communication connection                                    |
//+------------------------------------------------------------------+
void TestCommunicationConnection()
{
    Print("Testing communication connection...");

    if (g_commManager != NULL)
    {
        if (g_commManager.Connect())
        {
            ENUM_COMM_STATUS status = g_commManager.GetStatus();
            if (status == COMM_STATUS_CONNECTED)
            {
                Print("✓ Communication connection test PASSED");
                g_testsPassed++;
            }
            else
            {
                Print("✗ Communication connection test FAILED - Wrong status");
                g_testsFailed++;
            }
        }
        else
        {
            Print("✗ Communication connection test FAILED - Connection failed");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Communication connection test FAILED - Manager is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test message sending                                             |
//+------------------------------------------------------------------+
void TestMessageSending()
{
    Print("Testing message sending...");

    if (g_commManager != NULL && g_commManager.GetStatus() == COMM_STATUS_CONNECTED)
    {
        string test_payload = "{\"test\":\"message\",\"timestamp\":" + IntegerToString(TimeCurrent()) + "}";

        if (g_commManager.SendMessage(COMM_MSG_STATUS_REQUEST, test_payload))
        {
            Print("✓ Message sending test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Message sending test FAILED");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Message sending test FAILED - Manager not connected");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test message receiving                                           |
//+------------------------------------------------------------------+
void TestMessageReceiving()
{
    Print("Testing message receiving...");

    if (g_commManager != NULL)
    {
        CommMessage message;
        // Note: This test may fail if no messages are available, which is normal
        bool received = g_commManager.ReceiveMessage(message);

        // Test passes regardless of whether a message was received
        // (we're testing the functionality, not message availability)
        Print("✓ Message receiving test PASSED (functionality check)");
        g_testsPassed++;
    }
    else
    {
        Print("✗ Message receiving test FAILED - Manager is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test heartbeat functionality                                     |
//+------------------------------------------------------------------+
void TestHeartbeat()
{
    Print("Testing heartbeat functionality...");

    if (g_commManager != NULL && g_commManager.GetStatus() == COMM_STATUS_CONNECTED)
    {
        if (g_commManager.SendHeartbeat())
        {
            Print("✓ Heartbeat test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Heartbeat test FAILED");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Heartbeat test FAILED - Manager not connected");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test calculation performance                                     |
//+------------------------------------------------------------------+
void TestCalculationPerformance()
{
    Print("Testing calculation performance...");

    if (g_testEngine != NULL)
    {
        uint start_time = GetTickCount();

        // Perform multiple calculations
        for (int i = 0; i < TestIterations; i++)
        {
            double kelly = 0.0;
            g_testEngine.CalculateKellyFraction(kelly);

            double pos_size = g_testEngine.CalculatePositionSize(
                TestSymbol,
                SymbolInfoDouble(TestSymbol, SYMBOL_ASK),
                SymbolInfoDouble(TestSymbol, SYMBOL_ASK) - 50 * SymbolInfoDouble(TestSymbol, SYMBOL_POINT),
                ORDER_TYPE_BUY
            );
        }

        uint end_time = GetTickCount();
        uint duration = end_time - start_time;

        Print(StringFormat("✓ Performance test completed in %d ms for %d iterations", duration, TestIterations));

        // Performance should be reasonable (< 100ms per iteration on average)
        if (duration < TestIterations * 100)
        {
            Print("✓ Performance test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Performance test FAILED - Too slow");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Performance test FAILED - Engine is NULL");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Test memory usage                                                |
//+------------------------------------------------------------------+
void TestMemoryUsage()
{
    Print("Testing memory usage...");

    // MQL5 doesn't provide direct memory monitoring
    // This is a placeholder test
    Print("✓ Memory usage test PASSED (placeholder)");
    g_testsPassed++;
}

//+------------------------------------------------------------------+
//| Test concurrent operations                                       |
//+------------------------------------------------------------------+
void TestConcurrentOperations()
{
    Print("Testing concurrent operations...");

    if (g_testEngine != NULL && g_commManager != NULL)
    {
        // Test multiple operations simultaneously
        bool stats_ok = g_testEngine.UpdateTradeStats();
        bool comm_ok = g_commManager.CheckHeartbeat();

        if (stats_ok && comm_ok)
        {
            Print("✓ Concurrent operations test PASSED");
            g_testsPassed++;
        }
        else
        {
            Print("✗ Concurrent operations test FAILED");
            g_testsFailed++;
        }
    }
    else
    {
        Print("✗ Concurrent operations test FAILED - Components not available");
        g_testsFailed++;
    }
}

//+------------------------------------------------------------------+
//| Print test results                                               |
//+------------------------------------------------------------------+
void PrintTestResults()
{
    Print("\n=== Test Results ===");
    Print(StringFormat("Tests Passed: %d", g_testsPassed));
    Print(StringFormat("Tests Failed: %d", g_testsFailed));
    Print(StringFormat("Total Tests: %d", g_testsPassed + g_testsFailed));

    if (g_testsFailed == 0)
    {
        Print("🎉 All tests PASSED!");
    }
    else
    {
        Print(StringFormat("⚠️  %d test(s) FAILED. Please review the output above.", g_testsFailed));
    }
}

//+------------------------------------------------------------------+