#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QComboBox>
#include <QPushButton>
#include <QProgressBar>
#include <QTextEdit>
#include <QLabel>
#include <QProcess>
#include <QFileDialog>
#include <QMessageBox>
#include <QRadioButton>
#include <QButtonGroup>
#include <QRegularExpression>

class DdGui : public QWidget {
    Q_OBJECT
public:
    DdGui(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("dd_gui - Debian 13");
        resize(600, 650);

        auto *mainLayout = new QVBoxLayout(this);

        // 1. Bron Sectie
        mainLayout->addWidget(new QLabel("1. Bron (Input):"));
        auto *hIn = new QHBoxLayout();
        inputCombo = new QComboBox(this);
        inputCombo->setEditable(true);
        hIn->addWidget(inputCombo, 1);
        auto *btnFileIn = new QPushButton("Bestand...");
        hIn->addWidget(btnFileIn);
        mainLayout->addLayout(hIn);

        // 2. Doel Sectie
        mainLayout->addWidget(new QLabel("2. Doel (Output):"));
        auto *hOut = new QHBoxLayout();
        outputCombo = new QComboBox(this);
        outputCombo->setEditable(true);
        hOut->addWidget(outputCombo, 1);
        auto *btnFileOut = new QPushButton("Bestand...");
        hOut->addWidget(btnFileOut);
        mainLayout->addLayout(hOut);

        // 3. Blokgrootte
        mainLayout->addWidget(new QLabel("3. Blokgrootte (Snelheid):"));
        auto *hBs = new QHBoxLayout();
        bsGroup = new QButtonGroup(this);
        QStringList sizes = {"64K", "1M", "4M"};
        for (const QString &size : sizes) {
            auto *rb = new QRadioButton(size);
            if (size == "1M") rb->setChecked(true);
            bsGroup->addButton(rb);
            hBs->addWidget(rb);
        }
        mainLayout->addLayout(hBs);

        // 4. Progressie
        mainLayout->addWidget(new QLabel("Voortgang:"));
        progressBar = new QProgressBar(this);
        progressBar->setRange(0, 100);
        progressBar->setValue(0);
        progressBar->setTextVisible(true);
        // Standaard rood
        progressBar->setStyleSheet("QProgressBar::chunk { background-color: #ff4d4d; }");
        mainLayout->addWidget(progressBar);

        // 5. Log
        logText = new QTextEdit(this);
        logText->setReadOnly(true);
        logText->setStyleSheet("background-color: black; color: #00ff00; font-family: monospace;");
        mainLayout->addWidget(logText);

        // 6. Knoppen
        auto *hBtn = new QHBoxLayout();
        startBtn = new QPushButton("START CLONEN");
        stopBtn = new QPushButton("STOP");
        stopBtn->setEnabled(false);
        hBtn->addWidget(startBtn);
        hBtn->addWidget(stopBtn);
        mainLayout->addLayout(hBtn);

        connect(btnFileIn, &QPushButton::clicked, this, &DdGui::selectFileIn);
        connect(btnFileOut, &QPushButton::clicked, this, &DdGui::selectFileOut);
        connect(startBtn, &QPushButton::clicked, this, &DdGui::startDd);
        connect(stopBtn, &QPushButton::clicked, this, &DdGui::stopDd);

        refreshDevices();
        process = nullptr;
        totalBytes = 0;
    }

private slots:
    void refreshDevices() {
        QProcess lsblk;
        lsblk.start("lsblk", {"-dpno", "NAME,SIZE,MODEL"});
        if (lsblk.waitForFinished()) {
            QString output = lsblk.readAllStandardOutput();
            inputCombo->addItems(output.split("\n", Qt::SkipEmptyParts));
            outputCombo->addItems(output.split("\n", Qt::SkipEmptyParts));
        }
    }

    void selectFileIn() {
        QString f = QFileDialog::getOpenFileName(this, "Selecteer Bron");
        if(!f.isEmpty()) inputCombo->setCurrentText(f);
    }

    void selectFileOut() {
        QString f = QFileDialog::getSaveFileName(this, "Selecteer Doel");
        if(!f.isEmpty()) outputCombo->setCurrentText(f);
    }

    void startDd() {
        QString ifPath = inputCombo->currentText().split(" ").first();
        QString ofPath = outputCombo->currentText().split(" ").first();
        QString bs = bsGroup->checkedButton()->text();

        if(ifPath.isEmpty() || ofPath.isEmpty()) return;

        // Haal totale grootte op voor percentage
        QProcess sizeProc;
        sizeProc.start("lsblk", {"-dbno", "SIZE", ifPath});
        sizeProc.waitForFinished();
        totalBytes = sizeProc.readAllStandardOutput().trimmed().toLongLong();

        if (QMessageBox::warning(this, "Bevestiging", "Dit wist alle data op het doel. Doorgaan?", 
            QMessageBox::Yes | QMessageBox::No) != QMessageBox::Yes) return;

        process = new QProcess(this);
        process->setProcessChannelMode(QProcess::MergedChannels);

        connect(process, &QProcess::readyReadStandardOutput, this, &DdGui::readProgress);
        connect(process, &QProcess::finished, this, &DdGui::onFinished);

        process->start("sudo", {"stdbuf", "-oL", "dd", "if=" + ifPath, "of=" + ofPath, "bs=" + bs, "status=progress"});
        
        startBtn->setEnabled(false);
        stopBtn->setEnabled(true);
        progressBar->setValue(0);
        logText->clear();
    }

    void readProgress() {
        if (!process) return;
        QString data = process->readAllStandardOutput();
        logText->insertPlainText(data);
        logText->ensureCursorVisible();

        // Regex om bytes te vinden: zoek naar getal gevolgd door "bytes"
        static QRegularExpression re("(\\d+)\\s+bytes");
        QRegularExpressionMatch match = re.match(data);
        
        if (match.hasMatch() && totalBytes > 0) {
            long long currentBytes = match.captured(1).toLongLong();
            int progress = static_cast<int>((currentBytes * 100) / totalBytes);
            progressBar->setValue(progress);

            // Kleur aanpassen op basis van voortgang
            if (progress < 33) {
                progressBar->setStyleSheet("QProgressBar::chunk { background-color: #ff4d4d; }"); // Rood
            } else if (progress < 66) {
                progressBar->setStyleSheet("QProgressBar::chunk { background-color: #ffa500; }"); // Oranje
            } else {
                progressBar->setStyleSheet("QProgressBar::chunk { background-color: #28a745; }"); // Groen
            }
        }
    }

    void stopDd() {
        if(process) process->terminate();
    }

    void onFinished() {
        startBtn->setEnabled(true);
        stopBtn->setEnabled(false);
        progressBar->setValue(100);
        progressBar->setStyleSheet("QProgressBar::chunk { background-color: #28a745; }");
        QMessageBox::information(this, "Klaar", "Proces beëindigd.");
        process->deleteLater();
        process = nullptr;
    }

private:
    QComboBox *inputCombo, *outputCombo;
    QProgressBar *progressBar;
    QTextEdit *logText;
    QPushButton *startBtn, *stopBtn;
    QButtonGroup *bsGroup;
    QProcess *process;
    long long totalBytes;
};

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    DdGui w;
    w.show();
    return a.exec();
}

#include "main.moc"
