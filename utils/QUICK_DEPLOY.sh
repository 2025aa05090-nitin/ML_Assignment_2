#!/bin/bash

# Quick Deployment Script for ML Assignment 2

echo "============================================================"
echo "ML Assignment 2 - Quick Deployment Check"
echo "============================================================"
echo ""

# Check if we can run the app
echo "Step 1: Testing app components..."
python3 test_app.py

echo ""
echo "Step 2: Starting Streamlit app..."
echo "The app will open in your browser."
echo "Press Ctrl+C to stop the app."
echo ""
echo "============================================================"

streamlit run app.py
