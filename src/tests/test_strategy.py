import unittest
import pandas as pd
import numpy as np
from api.strategy.routing import calculate_ma_crossover_signals, calculate_performance

class TestStrategyCalculations(unittest.TestCase):
    def setUp(self):
        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        self.test_data = pd.DataFrame({
            'datetime': dates,
            'close': np.random.normal(100, 10, 100).cumsum()  # Random walk
        })

    def test_ma_crossover_signals(self):
        df = calculate_ma_crossover_signals(self.test_data, short_window=5, long_window=20)
        
        self.assertIn('short_ma', df.columns)
        self.assertIn('long_ma', df.columns)
        self.assertIn('signal', df.columns)
        self.assertIn('position', df.columns)
        
        self.assertTrue(df['signal'].isin([-1, 0, 1]).all())
        
        self.assertEqual(len(df[df['position'] != 0]), 
                        len(df[df['signal'].diff() != 0]))

    def test_performance_calculation(self):
        df = calculate_ma_crossover_signals(self.test_data)
        performance = calculate_performance(df)
        
        required_metrics = ['total_return', 'annual_return', 'sharpe_ratio', 
                          'total_trades', 'win_rate']
        for metric in required_metrics:
            self.assertIn(metric, performance)
        
        # Test if metrics have reasonable values
        self.assertIsInstance(performance['total_return'], float)
        self.assertIsInstance(performance['annual_return'], float)
        self.assertIsInstance(performance['sharpe_ratio'], float)
        self.assertIsInstance(performance['total_trades'], int)
        self.assertIsInstance(performance['win_rate'], float)
        self.assertTrue(0 <= performance['win_rate'] <= 1)

    def test_edge_cases(self):
        constant_data = pd.DataFrame({
            'datetime': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'close': [100] * 100
        })
        df = calculate_ma_crossover_signals(constant_data)
        self.assertEqual(len(df[df['signal'] != 0]), 0)
        
        increasing_data = pd.DataFrame({
            'datetime': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'close': range(100)
        })
        df = calculate_ma_crossover_signals(increasing_data)
        self.assertTrue(len(df[df['signal'] != 0]) > 0)

if __name__ == '__main__':
    unittest.main() 
