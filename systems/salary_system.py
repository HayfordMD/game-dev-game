import math
from datetime import datetime
from typing import Dict, Optional

class SalarySystem:
    """
    Manages NPC salary calculations based on skills and year.

    Base Rules (1978):
    - Minimum salary: $850/month
    - Max salary (60 skill points): $30,000/month
    - Formula: For skills < 60: $30k - ($1k * (60 - total_skills))
    - Annual increase: 3.5% compounding
    - Base hiring increase: $2,000/year from 1978

    Example calculations:
    - 60 skills in 1978: $30,000/month
    - 30 skills in 1978: $30,000 - (30 * $1,000) = $0 -> min $850
    - 60 skills in 2018: $30,000 + ($2,000 * 40 years) = $110,000/month (before 3.5% adjustments)
    """

    BASE_YEAR = 1978
    MIN_SALARY_1978 = 850  # Minimum monthly salary in 1978
    MAX_SKILL_POINTS = 60  # Maximum possible skill points (6 skills * 10 max)
    BASE_SALARY_1978 = 30000  # Base monthly salary for 60 skill points in 1978
    SKILL_PENALTY = 1000  # Salary reduction per skill point below 60
    ANNUAL_INCREASE_RATE = 0.035  # 3.5% annual increase
    BASE_HIRING_INCREASE = 2000  # Additional base salary per year after 1978

    @staticmethod
    def calculate_total_skills(npc_data: Dict) -> int:
        """Calculate total skill points for an NPC"""
        skills = npc_data.get('character', {}).get('skills', {})
        return sum([
            skills.get('engineering', 0),
            skills.get('marketing', 0),
            skills.get('leadership', 0),
            skills.get('design', 0),
            skills.get('research', 0),
            skills.get('communication', 0)
        ])

    @staticmethod
    def calculate_base_salary_for_year(total_skills: int, year: int) -> float:
        """
        Calculate base monthly salary for given skills and year.

        Args:
            total_skills: Sum of all 6 skill values (0-60)
            year: The year to calculate salary for

        Returns:
            Monthly salary in dollars
        """
        years_since_1978 = max(0, year - SalarySystem.BASE_YEAR)

        # Calculate base salary for the year
        if total_skills >= SalarySystem.MAX_SKILL_POINTS:
            # Max skills get full base salary
            base_for_year = SalarySystem.BASE_SALARY_1978 + (SalarySystem.BASE_HIRING_INCREASE * years_since_1978)
        else:
            # Reduce salary for lower skills
            skill_deficit = SalarySystem.MAX_SKILL_POINTS - total_skills
            base_for_1978 = SalarySystem.BASE_SALARY_1978 - (skill_deficit * SalarySystem.SKILL_PENALTY)

            # Ensure minimum salary in 1978
            base_for_1978 = max(SalarySystem.MIN_SALARY_1978, base_for_1978)

            # Add yearly base increase
            base_for_year = base_for_1978 + (SalarySystem.BASE_HIRING_INCREASE * years_since_1978)

        # Apply compounding annual increase
        final_salary = base_for_year * math.pow(1 + SalarySystem.ANNUAL_INCREASE_RATE, years_since_1978)

        # Ensure minimum salary adjusted for inflation
        min_salary_for_year = SalarySystem.MIN_SALARY_1978 * math.pow(1 + SalarySystem.ANNUAL_INCREASE_RATE, years_since_1978)

        return max(min_salary_for_year, final_salary)

    @staticmethod
    def calculate_npc_salary(npc_data: Dict, current_year: int,
                            hire_year: Optional[int] = None,
                            is_rehire: bool = False) -> Dict:
        """
        Calculate monthly salary for an NPC.

        Args:
            npc_data: NPC data dictionary with skills
            current_year: Current game year
            hire_year: Year the NPC was originally hired (for tenure calculations)
            is_rehire: Whether this is a rehire (30% discount applies)

        Returns:
            Dictionary with salary details
        """
        total_skills = SalarySystem.calculate_total_skills(npc_data)

        # Use hire year if provided, otherwise current year
        calculation_year = hire_year or current_year
        base_monthly = SalarySystem.calculate_base_salary_for_year(total_skills, calculation_year)

        # Apply rehire discount if applicable
        if is_rehire:
            base_monthly *= 0.7  # 30% discount

        # Calculate annual raises if they've been employed
        if hire_year and hire_year < current_year:
            years_employed = current_year - hire_year
            # Standard 3.5% raise per year of employment
            base_monthly *= math.pow(1 + SalarySystem.ANNUAL_INCREASE_RATE, years_employed)

        return {
            "monthly_salary": round(base_monthly, 2),
            "annual_salary": round(base_monthly * 12, 2),
            "total_skills": total_skills,
            "is_rehire": is_rehire,
            "hire_year": hire_year,
            "current_year": current_year
        }

    @staticmethod
    def get_market_rate(total_skills: int, year: int) -> float:
        """Get the market rate salary for a skill level in a given year"""
        return SalarySystem.calculate_base_salary_for_year(total_skills, year)

    @staticmethod
    def calculate_raise(current_salary: float, performance_multiplier: float = 1.0) -> float:
        """
        Calculate a raise based on performance.

        Args:
            current_salary: Current monthly salary
            performance_multiplier: 0.5 (poor) to 2.0 (excellent) performance

        Returns:
            New monthly salary after raise
        """
        base_raise = SalarySystem.ANNUAL_INCREASE_RATE
        actual_raise = base_raise * performance_multiplier
        return current_salary * (1 + actual_raise)

    @staticmethod
    def format_salary(salary: float) -> str:
        """Format salary for display"""
        if salary >= 1000:
            return f"${salary/1000:.1f}k/month"
        else:
            return f"${salary:.0f}/month"


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    print("=== Salary System Test Cases ===\n")

    salary_sys = SalarySystem()

    # Test 1: Max skills in 1978
    print("Test 1: Max skills (60) in 1978")
    salary = salary_sys.calculate_base_salary_for_year(60, 1978)
    print(f"Monthly: {salary_sys.format_salary(salary)}")
    print(f"Annual: ${salary*12:,.0f}\n")

    # Test 2: Average skills in 1978
    print("Test 2: Average skills (30) in 1978")
    salary = salary_sys.calculate_base_salary_for_year(30, 1978)
    print(f"Monthly: {salary_sys.format_salary(salary)}")
    print(f"Annual: ${salary*12:,.0f}\n")

    # Test 3: Low skills in 1978
    print("Test 3: Low skills (10) in 1978")
    salary = salary_sys.calculate_base_salary_for_year(10, 1978)
    print(f"Monthly: {salary_sys.format_salary(salary)}")
    print(f"Annual: ${salary*12:,.0f}\n")

    # Test 4: Max skills in 2018
    print("Test 4: Max skills (60) in 2018")
    salary = salary_sys.calculate_base_salary_for_year(60, 2018)
    print(f"Monthly: {salary_sys.format_salary(salary)}")
    print(f"Annual: ${salary*12:,.0f}\n")

    # Test 5: Test with actual NPC data
    print("Test 5: Christopher Adams (Game Designer)")
    npc_data = {
        'character': {
            'name': 'Christopher Adams',
            'skills': {
                'engineering': 1,
                'marketing': 2,
                'leadership': 3,
                'design': 7,
                'research': 4,
                'communication': 5
            }
        }
    }

    result = salary_sys.calculate_npc_salary(npc_data, 1985)
    print(f"Total skills: {result['total_skills']}")
    print(f"Monthly salary in 1985: {salary_sys.format_salary(result['monthly_salary'])}")
    print(f"Annual salary: ${result['annual_salary']:,.0f}\n")

    # Test 6: Rehire with discount
    print("Test 6: Same NPC rehired in 1990 (30% discount)")
    result = salary_sys.calculate_npc_salary(npc_data, 1990, is_rehire=True)
    print(f"Monthly salary: {salary_sys.format_salary(result['monthly_salary'])}")
    print(f"Annual salary: ${result['annual_salary']:,.0f}\n")

    # Test 7: Salary progression over years
    print("Test 7: Salary progression for 30 skill points")
    for year in [1978, 1985, 1995, 2005, 2015, 2025]:
        salary = salary_sys.calculate_base_salary_for_year(30, year)
        print(f"{year}: {salary_sys.format_salary(salary)}")