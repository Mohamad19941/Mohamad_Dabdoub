--Select*
--From dbo.CovidVaccination$
--order by 3,4


select Location, date, total_cases, new_cases, total_deaths, population
From PortfolioProject..CovidDeaths$

order by 1,2


---Looking at Total Cases vs Total Deaths


SELECT 
    Location, 
    date, 
    total_cases, 
    total_deaths, 
    CASE 
        WHEN TRY_CONVERT(int, total_cases) IS NOT NULL 
             AND TRY_CONVERT(int, total_deaths) IS NOT NULL 
             AND TRY_CONVERT(int, total_cases) != 0 
            THEN round((TRY_CONVERT(int, total_deaths) / TRY_CONVERT(float, total_cases)) * 100,2)
        ELSE NULL 
    END AS death_rate
FROM 
    PortfolioProject..CovidDeaths$
	Where location like '%Canada%'
ORDER BY 
    Location, date;


--- Looking at Total Cases vs Population


SELECT 
    Location, 
    date, 
    total_cases,
	population,
	Case
	when TRY_CONVERT(int, total_cases) IS NOT  NULL 
	Then (TRY_CONVERT(int, total_cases)/population)*100
	Else NULL
	End as Covid_rate
From PortfolioProject..CovidDeaths$
Group by Location, date
Order by
location, date;


--Looking at countries with heighest infection rate
Select
Location, Population, Max(total_cases) as HeighestInfd, Max((total_cases/Population))*100 as PercentPopulationInfected
from PortfolioProject..CovidDeaths$
where location != continent
Group by Location, Population 
order by PercentPopulationInfected desc




SELECT
    SUM(Population) AS TotalPopulation
FROM
    (
    SELECT
        Location,
        Population,
        MAX(total_cases) AS HeighestInfd,
        MAX((total_cases / Population)) * 100 AS PercentPopulationInfected
    FROM
        PortfolioProject..CovidDeaths$
    GROUP BY
        Location,
        Population 
    ) AS subquery;


Select 
	Sum(Population) as  TotalPopulation
	From (
			Select
			Location,
			Population
			From PortfolioProject..CovidDeaths$
			where location != continent
			Group by
			Location
			, Population
			) as subquery;


--Looking at countries with heighest death count per population

--Select
--Location, Population, Max(total_deaths) as Death, Max((total_deaths/Population))*100 as MaxDeathRate
--from PortfolioProject..CovidDeaths$
--Group by Location, Population
--order by MaxDeathRate desc

Select Location, Max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths$
where continent != location
Group by Location
order by TotalDeathCount desc



--- By continent

Select continent, Max(cast(total_deaths as int)) as TotalDeathCont
From PortfolioProject..CovidDeaths$
where continent is not null
Group by continent
order by TotalDeathCont desc



--- Global Numbers
SELECT 
    *,
    (RollingPeopleVaccinated / population) * 100 AS PercentageRollingPeopleVaccinated
FROM (
    SELECT 
        dea.continent, 
        dea.Location, 
        dea.date, 
        dea.population, 
        vac.new_vaccinations, 
        CASE 
            WHEN vac.new_vaccinations IS NOT NULL THEN 
                SUM(Try_convert(bigint, vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.Location, dea.Date) 
            ELSE 
                NULL 
        END AS RollingPeopleVaccinated
    FROM 
        PortfolioProject..CovidDeaths$ AS dea
    JOIN 
        PortfolioProject..CovidVaccination$ AS vac
    ON 
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE 
        dea.continent IS NOT NULL
) AS subquery
ORDER BY 
    Location, date;





Select

Location, Population, SUM(Try_convert(bigint, people_fully_vaccinated)) OVER (PARTITION BY Location) as Vaccinated

From (
Select 
	dea.Location, dea.date, dea.population, vac.people_fully_vaccinated
	From PortfolioProject..CovidDeaths$ as dea
	join
	PortfolioProject..CovidVaccination$ as vac
	    ON 
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE 
        dea.continent IS NOT NULL
	and vac.people_fully_vaccinated is not null
	
	) As subquery




Select Distinct
Location,
Population,
Vaccinated,
(Vaccinated/Population)*100 as VaccPercentage
from (

Select

	dea.Location, dea.date, dea.population, Try_convert(bigint, vac.total_boosters) as Vaccinated
	From PortfolioProject..CovidDeaths$ as dea
	join
	PortfolioProject..CovidVaccination$ as vac
	    ON 
        dea.location = vac.location
        AND dea.date = vac.date
    WHERE 
        dea.continent IS NOT NULL
	and vac.total_boosters is not null
	
	)As subquery



SELECT Distinct
    Location,
    SUM(CASE WHEN icu_patients IS NOT NULL THEN Try_convert(int, icu_patients) ELSE 0 END) OVER (PARTITION BY Location) AS ICU,
    SUM(CASE WHEN hosp_patients IS NOT NULL THEN Try_convert(int, hosp_patients) ELSE 0 END) OVER (PARTITION BY Location) AS HOSP
FROM
    PortfolioProject..CovidDeaths$
WHERE
    icu_patients IS NOT NULL AND hosp_patients IS NOT NULL


ORDER BY
    Location;



SELECT Distinct
    Location,
	date,
    icu_patients,
    hosp_patients
FROM
    PortfolioProject..CovidDeaths$
WHERE
    icu_patients IS NOT NULL AND hosp_patients IS NOT NULL
	and Location != continent

ORDER BY
    Location;



SELECT Distinct
    Location,
	date,
    new_cases_smoothed
FROM
    PortfolioProject..CovidDeaths$
WHERE
    new_cases_smoothed IS NOT NULL
	and Location != continent

ORDER BY
    Location,date;





 