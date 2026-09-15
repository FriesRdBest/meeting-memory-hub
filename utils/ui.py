/* Signal-themed loading animation */
@keyframes mmcSignalPulse {
    0%, 100% {
        opacity: 0.25;
        transform: scale(0.98);
    }
    50% {
        opacity: 1;
        transform: scale(1.02);
    }
}

.mmc-signal-loader {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2.5rem 1rem;
}

.mmc-signal-dot {
    width: 0.7rem;
    height: 0.7rem;
    border-radius: 50%;
    background: rgba(47, 53, 255, 0.9);
    box-shadow: 0 0 12px rgba(47, 53, 255, 0.6);
    animation: mmcSignalPulse 1.2s ease-in-out infinite;
}

.mmc-signal-dot:nth-child(2) {
    animation-delay: 0.15s;
}

.mmc-signal-dot:nth-child(3) {
    animation-delay: 0.3s;
}

.mmc-signal-loader-label {
    color: var(--mmc-muted);
    font-size: 0.9rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
