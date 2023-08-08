from fastapi.testclient import TestClient
from fastapi import status
from app import app

import unittest

class TestDepositCalculation(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = TestClient(app=app) 

    # Correct period interval
    def test_min_periods_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 1,
            "amount": 10000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 10050.0
        }
    
    def test_max_periods_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 60,
            "amount": 10000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 10050.0, "28.02.2021": 10100.25, "31.03.2021": 10150.75, "30.04.2021": 10201.5,
            "31.05.2021": 10252.51, "30.06.2021": 10303.77, "31.07.2021": 10355.29, "31.08.2021": 10407.07,
            "30.09.2021": 10459.11, "31.10.2021": 10511.41, "30.11.2021": 10563.97, "31.12.2021": 10616.79,
            "31.01.2022": 10669.87, "28.02.2022": 10723.22, "31.03.2022": 10776.84, "30.04.2022": 10830.72,
            "31.05.2022": 10884.87, "30.06.2022": 10939.29, "31.07.2022": 10993.99, "31.08.2022": 11048.96,
            "30.09.2022": 11104.2, "31.10.2022": 11159.72, "30.11.2022": 11215.52, "31.12.2022": 11271.6,
            "31.01.2023": 11327.96, "28.02.2023": 11384.6, "31.03.2023": 11441.52, "30.04.2023": 11498.73,
            "31.05.2023": 11556.22, "30.06.2023": 11614.0, "31.07.2023": 11672.07, "31.08.2023": 11730.43,
            "30.09.2023": 11789.08, "31.10.2023": 11848.03, "30.11.2023": 11907.27, "31.12.2023": 11966.81,
            "31.01.2024": 12026.64, "29.02.2024": 12086.77, "31.03.2024": 12147.2, "30.04.2024": 12207.94, 
            "31.05.2024": 12268.98, "30.06.2024": 12330.32, "31.07.2024": 12391.97, "31.08.2024": 12453.93, 
            "30.09.2024": 12516.2, "31.10.2024": 12578.78, "30.11.2024": 12641.67, "31.12.2024": 12704.88, 
            "31.01.2025": 12768.4, "28.02.2025": 12832.24, "31.03.2025": 12896.4, "30.04.2025": 12960.88, 
            "31.05.2025": 13025.68, "30.06.2025": 13090.81, "31.07.2025": 13156.26, "31.08.2025": 13222.04, 
            "30.09.2025": 13288.15, "31.10.2025": 13354.59,"30.11.2025": 13421.36, "31.12.2025": 13488.47
        }

    # Correct amount interval
    def test_min_amount_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 5,
            "amount": 10000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 10050.0,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75,
            "30.04.2021": 10201.5,
            "31.05.2021": 10252.51
        }

    def test_max_amount_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 5,
            "amount": 3000000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 3015000.0,
            "28.02.2021": 3030075.0,
            "31.03.2021": 3045225.37,
            "30.04.2021": 3060451.5,
            "31.05.2021": 3075753.76
        }

    # Correct rate interval
    def test_min_rate_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 5,
            "amount": 10000,
            "rate": 1.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 10008.33,
            "28.02.2021": 10016.67,
            "31.03.2021": 10025.02,
            "30.04.2021": 10033.37,
            "31.05.2021": 10041.73
        }
    
    def test_max_rate_returns_correct(self):
        response = self.client.post('/deposit', json={
            "date": "31.01.2021",
            "periods": 5,
            "amount": 10000,
            "rate": 8.0
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "31.01.2021": 10066.67,
            "28.02.2021": 10133.78,
            "31.03.2021": 10201.34,
            "30.04.2021": 10269.35,
            "31.05.2021": 10337.81
        }

    # Errors
    def test_too_long_period_returns_exception(self):
        response = self.client.post('/deposit', json={
            "date": "31.03.2021",
            "periods": 600,
            "amount": 10000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_amount_is_too_large_returns_exception(self):
        response = self.client.post('/deposit', json={
            "date": "31.03.2021",
            "periods": 5,
            "amount": 10000000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_amount_is_too_small_returns_exception(self):
        response = self.client.post('/deposit', json={
            "date": "31.03.2021",
            "periods": 5,
            "amount": 5000,
            "rate": 6.0
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_rate_is_too_large_returns_exception(self):
        response = self.client.post('/deposit', json={
            "date": "31.03.2021",
            "periods": 5,
            "amount": 10000,
            "rate": 9.0
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_rate_is_too_small_returns_exception(self):
        response = self.client.post('/deposit', json={
            "date": "31.03.2021",
            "periods": 5,
            "amount": 10000,
            "rate": 0.5
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()

    def test_date_error_returns_exception(self):
        response = self.client.post('/deposit', json={
                "date": "33.01.2021",
                "periods": 6,
                "amount": 10000,
                "rate": 6.0
            })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_error_in_date_type_returns_exception(self):
        response = self.client.post('/deposit', json={
                "date": {},
                "periods": 6,
                "amount": 10000,
                "rate": 6.0
            })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()

    def test_error_in_periods_type_returns_exception(self):
        response = self.client.post('/deposit', json={
                "date": '31.01.2021',
                "periods": "a",
                "amount": 10000,
                "rate": 6.0
            })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_error_in_amount_type_returns_exception(self):
        response = self.client.post('/deposit', json={
                "date": '31.01.2021',
                "periods": 5,
                "amount": "t",
                "rate": 6.0
            })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()
    
    def test_error_in_rate_type_returns_exception(self):
        response = self.client.post('/deposit', json={
                "date": '31.01.2021',
                "periods": 5,
                "amount": 10000,
                "rate": "y"
            })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.json()

if __name__ == '__main__':
    unittest.main()