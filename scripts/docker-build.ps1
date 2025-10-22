# RiskOptima Engine Docker Build Script
# Builds and runs the containerized application

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("build", "run", "stop", "logs", "clean")]
    [string]$Command = "run",

    [Parameter(Mandatory=$false)]
    [string]$Tag = "latest",

    [Parameter(Mandatory=$false)]
    [switch]$Detached
)

$imageName = "riskoptima-engine:$Tag"
$containerName = "riskoptima-engine-app"

Write-Host "RiskOptima Engine Docker Manager" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

function Test-Docker {
    try {
        $null = docker --version
        return $true
    } catch {
        Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
        Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        exit 1
    }
}

function Build-Image {
    Write-Host "Building Docker image: $imageName" -ForegroundColor Yellow
    Write-Host "This may take several minutes..." -ForegroundColor Yellow

    try {
        Push-Location $PSScriptRoot\..

        # Build the image
        docker build -t $imageName .

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker image built successfully" -ForegroundColor Green
        } else {
            Write-Host "❌ Docker build failed" -ForegroundColor Red
            exit 1
        }

    } catch {
        Write-Host "❌ Build error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    } finally {
        Pop-Location
    }
}

function Start-Container {
    Write-Host "Starting RiskOptima Engine container..." -ForegroundColor Yellow

    # Check if container already exists
    $existingContainer = docker ps -a --filter "name=$containerName" --format "{{.Names}}"
    if ($existingContainer) {
        Write-Host "Removing existing container..." -ForegroundColor Yellow
        docker rm -f $containerName 2>$null | Out-Null
    }

    # Run the container
    $runArgs = @(
        "run",
        "--name", $containerName,
        "-p", "8000:8000",
        "-p", "8501:8501",
        "-e", "PYTHONUNBUFFERED=1",
        "-v", "${PWD}/data:/app/data",
        "-v", "${PWD}/logs:/app/logs"
    )

    if ($Detached) {
        $runArgs += "--detach"
    }

    $runArgs += $imageName

    try {
        & docker $runArgs

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Container started successfully" -ForegroundColor Green
            Write-Host "" -ForegroundColor White
            Write-Host "Application URLs:" -ForegroundColor White
            Write-Host "  Frontend: http://localhost:8501" -ForegroundColor White
            Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
            Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White

            if ($Detached) {
                Write-Host "" -ForegroundColor White
                Write-Host "Container is running in detached mode" -ForegroundColor White
                Write-Host "Use '.\docker-build.ps1 -Command logs' to view logs" -ForegroundColor White
                Write-Host "Use '.\docker-build.ps1 -Command stop' to stop the container" -ForegroundColor White
            }
        } else {
            Write-Host "❌ Failed to start container" -ForegroundColor Red
            exit 1
        }

    } catch {
        Write-Host "❌ Container start error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

function Stop-Container {
    Write-Host "Stopping RiskOptima Engine container..." -ForegroundColor Yellow

    try {
        docker stop $containerName 2>$null | Out-Null
        docker rm $containerName 2>$null | Out-Null
        Write-Host "✅ Container stopped and removed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error stopping container: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Show-Logs {
    Write-Host "Showing container logs (press Ctrl+C to exit)..." -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow

    try {
        docker logs -f $containerName
    } catch {
        Write-Host "❌ Error showing logs: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Container may not be running. Use '.\docker-build.ps1 -Command run' to start it." -ForegroundColor Yellow
    }
}

function Clean-Images {
    Write-Host "Cleaning up Docker images..." -ForegroundColor Yellow

    try {
        # Remove stopped containers
        docker container prune -f | Out-Null

        # Remove dangling images
        docker image prune -f | Out-Null

        # Remove riskoptima images
        $images = docker images "riskoptima-engine" --format "{{.Repository}}:{{.Tag}}"
        if ($images) {
            $images | ForEach-Object {
                Write-Host "Removing image: $_" -ForegroundColor Yellow
                docker rmi $_ 2>$null | Out-Null
            }
        }

        Write-Host "✅ Cleanup completed" -ForegroundColor Green
    } catch {
        Write-Host "❌ Cleanup error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Main execution
Test-Docker

switch ($Command) {
    "build" {
        Build-Image
    }

    "run" {
        # Check if image exists, build if not
        $imageExists = docker images $imageName --format "{{.Repository}}"
        if (-not $imageExists) {
            Write-Host "Image not found, building first..." -ForegroundColor Yellow
            Build-Image
        }

        Start-Container
    }

    "stop" {
        Stop-Container
    }

    "logs" {
        Show-Logs
    }

    "clean" {
        Stop-Container
        Clean-Images
    }

    default {
        Write-Host "Usage: .\docker-build.ps1 [-Command] {build|run|stop|logs|clean} [-Tag tag] [-Detached]" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow
        Write-Host "Commands:" -ForegroundColor White
        Write-Host "  build   - Build the Docker image" -ForegroundColor White
        Write-Host "  run     - Run the container (builds if needed)" -ForegroundColor White
        Write-Host "  stop    - Stop and remove the container" -ForegroundColor White
        Write-Host "  logs    - Show container logs" -ForegroundColor White
        Write-Host "  clean   - Stop container and clean up images" -ForegroundColor White
        Write-Host "" -ForegroundColor Yellow
        Write-Host "Examples:" -ForegroundColor White
        Write-Host "  .\docker-build.ps1" -ForegroundColor White
        Write-Host "  .\docker-build.ps1 -Command build -Tag v1.0" -ForegroundColor White
        Write-Host "  .\docker-build.ps1 -Command run -Detached" -ForegroundColor White
    }
}